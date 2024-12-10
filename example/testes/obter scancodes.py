import virtualbox

# Obtém o mapeamento de scancodes do teclado
scancodes = virtualbox.library_ext.keyboard.IKeyboard.SCANCODES

# Exibe os scancodes disponíveis
for key, code in scancodes.items():
    print(f"Tecla: {key} -> Scancode: {code}")
