from PyQt6 import QtWidgets

from prog.translations import TRANSLATIONS
from prog.nodes import MovableRect, MovableEllipse

# TODO: quando o setup acontece, ele vai na mesma interface para ambos os gateways
# TODO: quando é setado para ser automatico, ele põe em manual e preenche os campos escrevendo automático, invés de ignorar
def setup_network(scene, language):
    translations = TRANSLATIONS
    texts = translations[language]

    all_items = [item for item in scene.items() if isinstance(item, (MovableRect, MovableEllipse))]
    
    root = None
    for item in all_items:
        if isinstance(item, MovableRect):
            connected_interfaces = set()
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
                interface['automatic'] = False
                if interface['name'] == 'enp0s8':
                    ip = f"192.168.{subnet_counter}.1"
                    if ip not in used_ips:
                        interface['ip'] = ip
                        interface['netmask'] = "255.255.255.0"
                        interface['network'] = f"192.168.{subnet_counter}.0"
                        interface['gateway'] = "0.0.0.0"
                        used_ips.add(ip)
                        subnet_counter += 1
        elif isinstance(node, MovableEllipse):
            interface = node.interfaces[0]
            interface['automatic'] = False
            ip = f"192.168.{subnet_counter-1}.{len(used_ips) % 254 + 1}"
            if ip not in used_ips:
                interface['ip'] = ip
                interface['netmask'] = "255.255.255.0"
                interface['network'] = f"192.168.{subnet_counter-1}.0"
                interface['gateway'] = f"192.168.{subnet_counter-1}.1"
                used_ips.add(ip)
        
        node.text_item.setPlainText(node.info_text())
        
        for connected_node, _ in node.get_connected_items():
            if connected_node.interfaces[0]['ip'] == "automático":
                configure_network(connected_node, subnet_counter)
    
    configure_network(root)
