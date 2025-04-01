from PyQt6 import QtWidgets

from prog.translations import TRANSLATIONS
from prog.nodes import MovableRect, MovableEllipse

# TODO: falta configurar a segunda interface, ta servindo como um cabo
def setup_network(scene, language):
    translations = TRANSLATIONS
    texts = translations[language]
    # Get all nodes from the scene
    all_items = [item for item in scene.items() if isinstance(item, (MovableRect, MovableEllipse))]
   
    # Find root node (MovableRect with connections only on enp0s8)
    root_node = None
    for item in all_items:
        if isinstance(item, MovableRect):
            has_enp0s8_only = False
            if hasattr(item, 'connections_by_interface'):
                # Check if only enp0s8 has connections
                if (len(item.connections_by_interface['enp0s8']) > 0 and
                    len(item.connections_by_interface['enp0s3']) == 0):
                    if root_node is None:  # First root found
                        root_node = item
                    else:  # Multiple roots found - error
                        QtWidgets.QMessageBox.warning(None, texts["error_1"], texts["error_3"])
                        return None
   
    if not root_node:
        QtWidgets.QMessageBox.warning(None, texts["error_1"], texts["error_4"])
        return None
    
    # Configure root node's enp0s8 interface
    for interface in root_node.interfaces:
        if interface['name'] == 'enp0s8':
            interface['automatic'] = False
            interface['ip'] = '192.168.0.1'
            interface['netmask'] = '255.255.255.0'
            interface['network'] = '192.168.0.0'
            #interface['gateway'] = '192.168.0.1'
            interface['broadcast'] = '192.168.0.255'
            break
   
    # Update the displayed text
    root_node.text_item.setPlainText(root_node.info_text())
    
    # Mapa para acompanhar redes já configuradas
    network_map = {
        'enp0s8': {
            'network': '192.168.0.0',
            'next_ip': 2  # Começando pelo .2 pois .1 é o gateway
        }
    }
    
    # Configurar interfaces dos outros nós - começando pelo nó raiz
    configured_nodes = set([root_node])
    nodes_to_process = [(root_node, None)]  # (nó, interface usada para conectar)
    
    # Função auxiliar para gerar o próximo IP em uma rede
    def get_next_ip(network_key, interface_name):
        if interface_name not in network_map:
            # Criar nova rede para esta interface
            last_octet = len(network_map) + 1
            network_map[interface_name] = {
                'network': f'192.168.{last_octet}.0',
                'next_ip': 1  # Começando do .1
            }
        
        network_info = network_map[interface_name]
        network_base = network_info['network'][:-2]  # Remove o '.0' do final
        ip = f"{network_base}.{network_info['next_ip']}"
        network_info['next_ip'] += 1
        
        return ip, network_info['network'], f"{network_base}.255"
    
    # Processamento breadth-first para configurar todos os nós conectados
    while nodes_to_process:
        current_node, connecting_interface = nodes_to_process.pop(0)
        
        # Obter todos os nós conectados a este nó
        for connected_item, interface_name in current_node.get_connected_items():
            # Se o item conectado já foi configurado, pular
            if connected_item in configured_nodes:
                continue
            
            # Determinar qual interface usar para configuração
            config_interface = interface_name
            if isinstance(current_node, MovableRect) and isinstance(connected_item, MovableRect):
                # Caso Gateway-Gateway: caso especial onde temos formato "iface1 <-> iface2"
                if ' <-> ' in interface_name:
                    # Pegar a interface correta com base no nó atual
                    if current_node == root_node:
                        # Se o nó atual é o raiz, usa a interface enp0s8
                        config_interface = 'enp0s8'
                    else:
                        # Para outros gateways, decide qual interface usar
                        parts = interface_name.split(' <-> ')
                        # Usa a primeira interface não conectada ao nó raiz
                        connected_to_root = False
                        for other_conn in current_node.connections:
                            if other_conn.start_item == root_node or other_conn.end_item == root_node:
                                connected_to_root = True
                                break
                        
                        if connected_to_root:
                            # Está conectado ao raiz, então use outra interface
                            config_interface = 'enp0s3' if 'enp0s8' in parts else 'enp0s8'
                        else:
                            # Não está conectado ao raiz, pode usar qualquer interface
                            config_interface = parts[0]
            
            # Configurar a interface do item conectado
            if isinstance(connected_item, MovableRect):
                # Gateway: configura a interface apropriada
                for interface in connected_item.interfaces:
                    if interface['name'] == config_interface:
                        next_ip, network, broadcast = get_next_ip(config_interface, config_interface)
                        interface['automatic'] = False
                        interface['ip'] = next_ip
                        interface['netmask'] = '255.255.255.0'
                        interface['network'] = network
                        interface['broadcast'] = broadcast
                        
                        # Para interfaces não conectadas diretamente à rede raiz,
                        # configure o gateway adequadamente
                        if config_interface != 'enp0s8' or current_node != root_node:
                            for curr_interface in current_node.interfaces:
                                if curr_interface['name'] == interface_name.split(' <-> ')[0]:
                                    interface['gateway'] = curr_interface['ip']
                                    break
                        
                        break
            else:
                # Host (MovableEllipse): configura sua única interface
                interface = connected_item.interfaces[0]
                next_ip, network, broadcast = get_next_ip('enp0s8', 'enp0s8')
                interface['automatic'] = False
                interface['ip'] = next_ip
                interface['netmask'] = '255.255.255.0'
                interface['network'] = network
                interface['broadcast'] = broadcast
                
                # Define o gateway como o IP do nó gateway conectado
                for curr_interface in current_node.interfaces:
                    if curr_interface['name'] == interface_name:
                        interface['gateway'] = curr_interface['ip']
                        break
            
            # Atualiza o texto exibido
            connected_item.text_item.setPlainText(connected_item.info_text())
            
            # Marca como configurado e adiciona à fila para processar seus vizinhos
            configured_nodes.add(connected_item)
            nodes_to_process.append((connected_item, config_interface))
    
    return root_node