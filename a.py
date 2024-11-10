import sys
import os

# Caminho relativo para a pasta do VirtualBox SDK
sdk_path = os.path.join(os.path.dirname(__file__), "sdk/bindings/xpcom/python")
sys.path.append(sdk_path)
import vboxapi

# Inicializar a sessão do VirtualBox
vbox_mgr = vboxapi.VirtualBoxManager(None, None)
vbox = vbox_mgr.getVirtualBox()
session = vbox_mgr.getSessionObject(vbox)

# Nome da máquina a ser clonada
#source_vm_name = "Debian 12 https"
source_vm_name = "debian 10 seg"

# Nome da nova máquina clonada
clone_vm_name = "NomeDaVMClone"

# Localizar a máquina virtual original
source_vm = vbox.findMachine(source_vm_name)

# Criar a nova máquina clonada (alteração no settingsFilePath para None)
clone_vm = vbox.createMachine(None, clone_vm_name, [], source_vm.OSTypeId, "", "", "", "")

# Adicionar a nova máquina ao VirtualBox
vbox.registerMachine(clone_vm)

clone_vm = vbox.findMachine(clone_vm_name)
# Iniciar o processo de clonagem
#source_vm.lockMachine(session, vboxapi.constants.LockType_Shared)
source_vm.lockMachine(session, 1)
try:
    #progress = source_vm.cloneTo(clone_vm, vboxapi.constants.CloneMode_MachineState, [])
    progress = source_vm.cloneTo(clone_vm, 1, [])
    progress.waitForCompletion(-1)  # Aguarda o término da clonagem
finally:
    session.unlockMachine()

print(f"A máquina {clone_vm_name} foi clonada com sucesso.")
