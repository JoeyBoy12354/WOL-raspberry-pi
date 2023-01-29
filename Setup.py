import os
import time
import csv


cfd = os.path.dirname(os.path.realpath(__file__)) #Current file path
bootFile = '/etc/xdg/lxsession/LXDE-pi/autostart'
default1='@lxpanel --profile LXDE-pi \n'
default2='@pcmanfm --desktop --profile LXDE-pi \n'
default3='@xscreensaver -no-splash \n'
entry='@lxterminal -e python '+cfd+"/UI.py \n"

  
def getUpdates():
    response = os.system('sudo apt-get update')
    response = os.system('sudo apt-get upgrade')

def getModules(modules):
    outputlist = []
    # Iterate over all the modules in the list and install each module
    for module in modules:
        print("Getting: ",module)
        response = os.system('pip install ' + module)
        print("Response: ",response)
        print(" ")
    return

def setBootOnStart():
    print("The boot file will now open")
    time.sleep(3)
    print("PRESS \"Ctrl+X\" when it opens!")
    time.sleep(4)
    
    response = os.system('sudo nano '+bootFile)
    bootObj = open(bootFile, 'w')
    bootObj.writelines([default1,default2,default3,entry])
    bootObj.close()
    
    print("Your raspberry PI will now reboot") 
    time.sleep(5)
    response = os.system('sudo reboot')

    return
    
  
if __name__ == '__main__': 
    print("Setup for WOL-Johann_Strydom is starting...")
    time.sleep(2)

    # Get the list of modules from the text file
    modules = list(open('modules.txt'))
    # Iterate over all the modules that we read from the text file
    # and remove all the extra lines. This is just a preprocessing step
    # to make sure there aren't any unnecessary lines.
    for i in range(len(modules)):
        modules[i] = modules[i].strip('\n')

    print("Phase 0: Check for updates")
    getUpdates()
    print("")
    print("Phase 1: Installing Dependencies")
    getModules(modules) 
    print("")
    print("Phase 2: Setting software to boot on start")
    time.sleep(2)
    setBootOnStart()
    
