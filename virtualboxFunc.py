from nodes import NetworkShape
import virtualbox, time

def cloneConfigureMachines(selected_vm, scene):
    # Inicializar a sessão do VirtualBox
    vbox = virtualbox.VirtualBox()

    # Localizar a máquina virtual original
    source_vm = vbox.find_machine(selected_vm)
    machine_name_comp = 1

    # Itera sobre todos os itens da cena
    for item in scene.items():
        if isinstance(item, NetworkShape):  # Verifica se o item é uma forma com parâmetros de rede               

            clone_name = f"{selected_vm} {machine_name_comp}"

            # Criar a nova máquina clonada
            clone_vm = vbox.create_machine(name=clone_name, os_type_id=source_vm.os_type_id, settings_file="", groups=[], flags="")

            # Lock para iniciar o processo de clonagem
            session = virtualbox.Session()
            source_vm.lock_machine(session, virtualbox.library.LockType.shared)

            try:
                # Clonar a máquina
                print("Iniciando o processo de clonagem...")
                progress = source_vm.clone_to(target=clone_vm, mode=virtualbox.library.CloneMode.machine_state, options=[])
                
                max_wait_time = 600  # Tempo máximo em segundos (10 minutos 600)
                elapsed_time = 0
                
                while not progress.completed and elapsed_time < max_wait_time:
                    print(f"Progresso: {progress.percent}%, Operação atual: {progress.operation_description}")
                    time.sleep(1)  # Pausa para evitar um loop de polling intenso
                    elapsed_time += 1

                if not progress.completed:
                    print("A clonagem parece estar demorando demais. Verifique o sistema.")
                    progress.cancel()
                else:
                    # Registrar a nova máquina
                    vbox.register_machine(clone_vm)
            
            finally:
                # Liberar o lock
                session.unlock_machine()
                machine_name_comp = machine_name_comp + 1
            
            session = virtualbox.Session()
            # Encontra a máquina virtual pelo nome
            machine = vbox.find_machine(clone_name)

            # Inicia a máquina virtual em modo GUI
            progress = machine.launch_vm_process(session, "gui", [])
            progress.wait_for_completion()

            # Aguarda alguns segundos para a máquina inicializar até a tela de login
            time.sleep(30)  # Ajuste o tempo conforme necessário

            # Obtém o teclado da máquina virtual
            console = session.console
            keyboard = console.keyboard

            # Define as credenciais
            username = "root"
            password = "root"

            # Insere o usuário e a senha simulando a entrada pelo teclado
            keyboard.put_keys(username)
            keyboard.put_keys(["ENTER"])
            time.sleep(1)  # Tempo para o sistema processar
            keyboard.put_keys(password)
            keyboard.put_keys(["ENTER"])

            # Espera 5 segundos antes de abrir o terminal
            time.sleep(5)

            # Simula a abertura do terminal (Alt+F2 e comando lxterminal)
            keyboard.put_keys(hold_keys=["ALT"], press_keys=["F2"])
            time.sleep(1)  # Aguarda o menu abrir
            keyboard.put_keys("lxterminal")
            keyboard.put_keys(["ENTER"])

            time.sleep(1)  # Aguarda o menu abrir

            keyboard.put_keys("setxkbmap us\n")
            keyboard.put_keys('echo "" > /etc/network/interfaces\n')
            keyboard.put_keys("nano /etc/network/interfaces\n")

            time.sleep(1)

            keyboard.put_keys("source /etc/network/interfaces.d/*\n\n")
                    
            # Configuração da interface de loopback
            keyboard.put_keys("auto lo\n")
            keyboard.put_keys("iface lo inet loopback\n\n")
            
            # Itera sobre cada interface
            for iface in item.interfaces:
                # Especifica a interface como `auto` para habilitação
                keyboard.put_keys(f"auto {iface['name']}\n")
                
                # Configura a interface com `dhcp` ou `static`
                if iface.get("automatic", True):  # Se for automático, utiliza DHCP
                    keyboard.put_keys(f"iface {iface['name']} inet dhcp\n\n")
                else:  # Se for manual, configura como estático
                    keyboard.put_keys(f"iface {iface['name']} inet static\n")
                    
                    # Adiciona os campos conforme a interface
                    if iface['name'] == "enp0s8":  # enp0s8 com campos padrão e gateway opcional
                        keyboard.put_keys(f"    address {iface.get('ip', '')}\n")
                        keyboard.put_keys(f"    netmask {iface.get('netmask', '')}\n")
                        keyboard.put_keys(f"    network {iface.get('network', '')}\n")
                        if 'gateway' in iface:
                            keyboard.put_keys(f"    gateway {iface.get('gateway', '')}\n")
                    elif iface['name'] == "enp0s3":  # enp0s3 com broadcast adicional
                        keyboard.put_keys(f"    address {iface.get('ip', '')}\n")
                        keyboard.put_keys(f"    netmask {iface.get('netmask', '')}\n")
                        keyboard.put_keys(f"    network {iface.get('network', '')}\n")
                        keyboard.put_keys(f"    broadcast {iface.get('broadcast', '')}\n")
                    
                    keyboard.put_keys("\n")  # Separador entre as interfaces

            keyboard.put_keys(hold_keys=["CTRL"], press_keys=["o"])
            time.sleep(1)
            keyboard.put_keys(["ENTER"])
            time.sleep(1)
            keyboard.put_keys(hold_keys=["CTRL"], press_keys=["x"])
            time.sleep(1)
            keyboard.put_keys(["ENTER"])
            time.sleep(1)
            keyboard.put_keys("systemctl restart networking\n")
            time.sleep(2)

            if item.ip_forward == 1:
                keyboard.put_keys('echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf\n')

            keyboard.put_keys("setxkbmap br\n")
            time.sleep(1)  # Aguarda o menu abrir
            keyboard.put_keys("poweroff")
            keyboard.put_keys(["ENTER"])
            #session.console.power_down()
            session.unlock_machine()

def generate_files(self):
        """ Ordenação pelo Z-Value: Os itens com valores de Z menores 
        aparecem antes no loop. Isso reflete a "profundidade" dos 
        itens na cena (itens com Z menor são mais "atrás", e com Z 
                    maior são mais "na frente").

        Ordem de Adição: Para itens com o mesmo Z-Value, a ordem 
        será baseada na sequência em que foram adicionados à cena. 
        O primeiro item adicionado com um determinado Z-Value será 
        iterado antes dos outros. """

        # Itera sobre todos os itens da cena
        for item in self.scene.items():
            if isinstance(item, NetworkShape):  # Verifica se o item é uma forma com parâmetros de rede
                # Nome do arquivo baseado no IP da interface enp0s3 ou enp0s8, se disponível
                # file_name = f"{item.interfaces[0].get('ip', 'sem_ip')}_network_config.txt"
                file_name = "interfaces"
               
                # Abre o arquivo em modo de escrita
                with open(file_name, "w") as file:
                    # Escreve o cabeçalho do arquivo de configuração
                    file.write("source /etc/network/interfaces.d/*\n\n")
                    
                    # Configuração da interface de loopback
                    file.write("auto lo\n")
                    file.write("iface lo inet loopback\n\n")
                    
                    # Itera sobre cada interface
                    for iface in item.interfaces:
                        # Especifica a interface como `auto` para habilitação
                        file.write(f"auto {iface['name']}\n")
                        
                        # Configura a interface com `dhcp` ou `static`
                        if iface.get("automatic", True):  # Se for automático, utiliza DHCP
                            file.write(f"iface {iface['name']} inet dhcp\n\n")
                        else:  # Se for manual, configura como estático
                            file.write(f"iface {iface['name']} inet static\n")
                            
                            # Adiciona os campos conforme a interface
                            if iface['name'] == "enp0s8":  # enp0s8 com campos padrão e gateway opcional
                                file.write(f"    address {iface.get('ip', '')}\n")
                                file.write(f"    netmask {iface.get('netmask', '')}\n")
                                file.write(f"    network {iface.get('network', '')}\n")
                                if 'gateway' in iface:
                                    file.write(f"    gateway {iface.get('gateway', '')}\n")
                            elif iface['name'] == "enp0s3":  # enp0s3 com broadcast adicional
                                file.write(f"    address {iface.get('ip', '')}\n")
                                file.write(f"    netmask {iface.get('netmask', '')}\n")
                                file.write(f"    network {iface.get('network', '')}\n")
                                file.write(f"    broadcast {iface.get('broadcast', '')}\n")
                            
                            file.write("\n")  # Separador entre as interfaces
                   