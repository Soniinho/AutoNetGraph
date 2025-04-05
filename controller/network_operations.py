from PyQt6 import QtWidgets

from model.translations import TRANSLATIONS
from model import MovableRect, MovableEllipse


#@ funcionando, necessário mais testes
def setup_network(scene, language):
    translations = TRANSLATIONS
    texts = translations[language]
    # Get all nodes from the scene
    all_items = [item for item in scene.items() if isinstance(item, (MovableRect, MovableEllipse))]
   
    # Find root node (MovableRect with connections only on enp0s3)
    root_node = None
    for item in all_items:
        if isinstance(item, MovableRect):
            has_enp0s3_only = False
            if hasattr(item, 'connections_by_interface'):
                # Check if only enp0s3 has connections
                if (len(item.connections_by_interface['enp0s3']) > 0 and
                    len(item.connections_by_interface['enp0s8']) == 0):
                    if root_node is None:  # First root found
                        root_node = item
                    else:  # Multiple roots found - error
                        QtWidgets.QMessageBox.warning(None, texts["error_1"], texts["error_3"])
                        return None
   
    if not root_node:
        QtWidgets.QMessageBox.warning(None, texts["error_1"], texts["error_4"])
        return None
    
    # Configure root node's enp0s3 interface
    for interface in root_node.interfaces:
        if interface['name'] == 'enp0s3':
            interface['automatic'] = False  # Certifique-se de definir como False
            interface['ip'] = '192.168.1.1'
            interface['netmask'] = '255.255.255.0'
            interface['network'] = '192.168.1.0'
            interface['gateway'] = '192.168.1.1'
            interface['broadcast'] = '192.168.1.255'
            break
   
    # Update the displayed text
    root_node.text_item.setPlainText(root_node.info_text())
    
    # Mapa para acompanhar redes já configuradas
    network_map = {
        '192.168.1.0': {
            'next_ip': 2  # Começando pelo .2 pois .1 é o gateway
        }
    }
    
    # Contador para gerar novos IDs de rede
    next_network_id = 2
    
    # Mapa que associa um nó e uma interface a uma rede
    node_interface_network = {
        (root_node, 'enp0s3'): '192.168.1.0'
    }
    
    # Configurar interfaces dos outros nós - começando pelo nó raiz
    configured_nodes = set([root_node])
    nodes_to_process = [(root_node, None)]  # (nó, interface usada para conectar)
    
    # Função auxiliar para gerar o próximo IP em uma rede
    def get_next_ip(network_id):
        if network_id not in network_map:
            # Criar nova rede
            network_map[network_id] = {
                'next_ip': 1  # Começando do .1
            }
        
        network_info = network_map[network_id]
        network_base = network_id[:-2]  # Remove o '.0' do final
        ip = f"{network_base}.{network_info['next_ip']}"
        network_info['next_ip'] += 1
        
        return ip, network_id, f"{network_base}.255"
    
    # Função para gerar uma nova rede
    def create_new_network():
        nonlocal next_network_id
        new_network = f'192.168.{next_network_id}.0'
        next_network_id += 1
        return new_network
    
    # Processamento breadth-first para configurar todos os nós conectados
    while nodes_to_process:
        current_node, connecting_interface = nodes_to_process.pop(0)
        
        # Obter todos os nós conectados a este nó
        for connected_item, interface_name in current_node.get_connected_items():
            # Se o item conectado já foi configurado, pular
            if connected_item in configured_nodes:
                continue
            
            # Determinar qual interface do nó atual e do nó conectado usar
            current_node_interface = interface_name
            connected_node_interface = 'enp0s3' if interface_name == 'enp0s8' else 'enp0s8'
            
            # Caso especial gateway-gateway
            if isinstance(current_node, MovableRect) and isinstance(connected_item, MovableRect):
                if ' <-> ' in interface_name:
                    parts = interface_name.split(' <-> ')
                    current_node_interface = parts[0]
                    connected_node_interface = parts[1]
            
            # Determinar a rede a ser usada
            if (current_node, current_node_interface) in node_interface_network:
                # Usar a rede já associada à interface do nó atual
                network_id = node_interface_network[(current_node, current_node_interface)]
            else:
                # Criar nova rede para esta interface
                network_id = create_new_network()
                node_interface_network[(current_node, current_node_interface)] = network_id
            
            # Configurar a interface do item conectado
            if isinstance(connected_item, MovableRect):
                # Gateway: configura a interface apropriada
                interface_updated = False
                other_interface_updated = False
                
                for interface in connected_item.interfaces:
                    if interface['name'] == connected_node_interface:
                        # Se esta interface já está configurada, pular
                        if interface.get('ip') and not interface.get('automatic', True):
                            continue
                        
                        # Configurar esta interface com a rede atual
                        next_ip, network, broadcast = get_next_ip(network_id)
                        interface['automatic'] = False  # Importante: definir explicitamente como False
                        interface['ip'] = next_ip
                        interface['netmask'] = '255.255.255.0'
                        interface['network'] = network
                        interface['broadcast'] = broadcast
                        interface_updated = True
                        
                        # Associar esta interface à rede atual
                        node_interface_network[(connected_item, connected_node_interface)] = network_id
                        
                        # Configure gateway se necessário
                        for curr_interface in current_node.interfaces:
                            if curr_interface['name'] == current_node_interface:
                                interface['gateway'] = curr_interface['ip']
                                break
                
                # Configurar outra interface com uma NOVA rede (importante!)
                other_interface_name = 'enp0s8' if connected_node_interface == 'enp0s3' else 'enp0s3'
                for other_interface in connected_item.interfaces:
                    if other_interface['name'] == other_interface_name:
                        # Se esta interface já está configurada, pular
                        if other_interface.get('ip') and not other_interface.get('automatic', True):
                            continue
                        
                        # Criar uma nova rede para a outra interface
                        new_network_id = create_new_network()
                        next_ip, network, broadcast = get_next_ip(new_network_id)
                        other_interface['automatic'] = False  # Importante: definir explicitamente como False
                        other_interface['ip'] = next_ip
                        other_interface['netmask'] = '255.255.255.0'
                        other_interface['network'] = network
                        other_interface['gateway'] = other_interface['ip']
                        other_interface['broadcast'] = broadcast
                        other_interface_updated = True
                        
                        # Associar esta interface à nova rede
                        node_interface_network[(connected_item, other_interface_name)] = new_network_id
                        break
                
                # Apenas atualize o texto se alguma interface foi atualizada
                if interface_updated or other_interface_updated:
                    # Atualiza o texto exibido
                    connected_item.text_item.setPlainText(connected_item.info_text())
            else:
                # Host (MovableEllipse): configura sua única interface
                interface = connected_item.interfaces[0]
                if not interface.get('ip') or interface.get('automatic', True):
                    next_ip, network, broadcast = get_next_ip(network_id)
                    interface['automatic'] = False  # Importante: definir explicitamente como False
                    interface['ip'] = next_ip
                    interface['netmask'] = '255.255.255.0'
                    interface['network'] = network
                    interface['broadcast'] = broadcast
                    
                    # Define o gateway como o IP do nó gateway conectado
                    for curr_interface in current_node.interfaces:
                        if curr_interface['name'] == current_node_interface:
                            interface['gateway'] = curr_interface['ip']
                            break
                    
                    # Atualiza o texto exibido
                    connected_item.text_item.setPlainText(connected_item.info_text())
            
            # Marca como configurado e adiciona à fila para processar seus vizinhos
            configured_nodes.add(connected_item)
            nodes_to_process.append((connected_item, None))