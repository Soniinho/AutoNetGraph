import sys
import os

# Caminho relativo para a pasta do VirtualBox SDK
sdk_path = os.path.join(os.path.dirname(__file__), 'sdk/bindings/xpcom/python')
sys.path.append(sdk_path)

import vboxapi

mgr = vboxapi.VirtualBoxManager(None, None)
vbox = mgr.getVirtualBox()
name = "Debian 12 https"
mach = vbox.findMachine(name)
session = mgr.getSessionObject(vbox)

# Lançando a VM
progress = mach.launchVMProcess(session, "gui", [])
progress.waitForCompletion(-1)  # Aguarde a conclusão do processo
mgr.closeMachineSession(session)  # Feche a sessão após o uso

""" mgr = vboxapi.VirtualBoxManager(None, None)
vbox = mgr.getVirtualBox()
for m in mgr.getArray(vbox, 'machines'):
    print ("Machine '%s' logs in '%s'" %(m.name, m.logFolder)) """

