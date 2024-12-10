import time
import virtualbox

# Inicializa a instância do VirtualBox
vbox = virtualbox.VirtualBox()
session = virtualbox.Session()

# Encontra a máquina virtual pelo nome
machine = vbox.find_machine("VM2 yay")

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
keyboard.put_keys("poweroff")
keyboard.put_keys(["ENTER"])
#session.console.power_down()
session.unlock_machine()
