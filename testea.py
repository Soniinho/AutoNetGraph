import virtualbox
vbox = virtualbox.VirtualBox()
print ([m.name for m in vbox.machines])