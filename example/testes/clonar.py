import virtualbox
import time

# Inicializar a sessão do VirtualBox
vbox = virtualbox.VirtualBox()

# Nome da máquina a ser clonada
source_vm_name = "VM1"

# Nome da nova máquina clonada
clone_vm_name = "VM2 yay"

# Localizar a máquina virtual original
source_vm = vbox.find_machine(source_vm_name)

# Criar a nova máquina clonada
clone_vm = vbox.create_machine(name=clone_vm_name, os_type_id=source_vm.os_type_id, settings_file="", groups=[], flags="")

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

    # if progress.error_info is not None:
    #     print(f"Erro durante a clonagem: {progress.error_info.text}")
    # else:
    #     print(f"A máquina {clone_vm_name} foi clonada com sucesso.")
    
    # progress.wait_for_completion(-1)  # Aguarda o término da clonagem
  
finally:
    # Liberar o lock
    session.unlock_machine()
