from PyQt6 import QtWidgets

from prog.translations import TRANSLATIONS
from prog.nodes import MovableRect, MovableEllipse

# TODO: feito até o root node, precisa fazer iteração entre cada nó
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
