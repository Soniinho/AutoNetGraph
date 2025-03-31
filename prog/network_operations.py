from PyQt6 import QtWidgets

from prog.translations import TRANSLATIONS
from prog.nodes import MovableRect, MovableEllipse

# TODO: falta ele configurar a enp0s3, e não está configurando corretamente, tentar parte a parte
def setup_network(scene, language):
    translations = TRANSLATIONS
    texts = translations[language]

    all_items = [item for item in scene.items() if isinstance(item, (MovableRect, MovableEllipse))]
    
    root = None
    for item in all_items:
        if isinstance(item, MovableRect):
            connected_interfaces = set()
            
            # Usar o novo sistema de conexões por interface, se disponível
            if hasattr(item, 'connections_by_interface'):
                for interface_name, connections in item.connections_by_interface.items():
                    if connections:
                        connected_interfaces.add(interface_name)
            else:
                # Fallback para o sistema antigo
                for conn in item.connections:
                    if conn.interface_name:
                        connected_interfaces.add(conn.interface_name)
                        
            if len(connected_interfaces) == 1:
                if root is None:
                    root = item
                else:
                    QtWidgets.QMessageBox.warning(None, texts["error_1"], texts["error_3"])
                    return
    
    if not root:
        QtWidgets.QMessageBox.warning(None, texts["error_1"], texts["error_4"])
        return
    
    for item in all_items:
        if not item.has_valid_connections():
            QtWidgets.QMessageBox.warning(None, texts["error_1"], texts["error_5"])
            return
    
    used_ips = set()
    def configure_network(node, subnet_counter=1):
        if isinstance(node, MovableRect):
            for interface in node.interfaces:
                    if interface['name'] == 'enp0s8':
                        ip = f"192.168.{subnet_counter}.1"
                        if ip not in used_ips:
                            interface['automatic'] = False
                            interface['ip'] = ip
                            interface['netmask'] = "255.255.255.0"
                            interface['network'] = f"192.168.{subnet_counter}.0"
                            interface['gateway'] = "0.0.0.0"
                            used_ips.add(ip)
                            subnet_counter += 1
        elif isinstance(node, MovableEllipse):
            interface = node.interfaces[0]
            ip = f"192.168.{subnet_counter-1}.{len(used_ips) % 254 + 1}"
            if ip not in used_ips:
                interface['automatic'] = False
                interface['ip'] = ip
                interface['netmask'] = "255.255.255.0"
                interface['network'] = f"192.168.{subnet_counter-1}.0"
                interface['gateway'] = f"192.168.{subnet_counter-1}.1"
                used_ips.add(ip)
        
        node.text_item.setPlainText(node.info_text())
        
        # Obter os nós conectados usando o sistema atualizado
        connected_items = []
        
        if isinstance(node, MovableRect) and hasattr(node, 'connections_by_interface'):
            # Usar o novo sistema de conexões por interface
            for interface_name, connections in node.connections_by_interface.items():
                for conn in connections:
                    connected_node = conn.start_item if conn.start_item != node else conn.end_item
                    interface_used = conn.interface_name
                    
                    # Extrair o nome da interface para conexões entre dois MovableRect
                    if '<->' in interface_used:
                        parts = interface_used.split(' <-> ')
                        interface_used = parts[1] if connected_node == conn.end_item else parts[0]
                    
                    connected_items.append((connected_node, interface_used))
        else:
            # Fallback para o sistema antigo
            for conn in node.connections:
                connected_node = conn.start_item if conn.start_item != node else conn.end_item
                interface_used = conn.interface_name
                connected_items.append((connected_node, interface_used))
        
        # Configurar os nós conectados
        for connected_node, interface_used in connected_items:
            # Verificar se o nó precisa ser configurado
            needs_config = False
            
            if isinstance(connected_node, MovableEllipse):
                interface = connected_node.interfaces[0]
                if interface['automatic'] and interface['ip'] == "automático":
                    needs_config = True
            elif isinstance(connected_node, MovableRect):
                # Encontrar a interface conectada
                for interface in connected_node.interfaces:
                    if interface['name'] == interface_used:
                        if interface['automatic'] and interface['ip'] == "automático":
                            needs_config = True
                        break
            
            if needs_config:
                configure_network(connected_node, subnet_counter)
    
    configure_network(root)