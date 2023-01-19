
import sys, struct, socket
#import RPi.GPIO as GPIO
import time
from wakeonlan import send_magic_packet
import os
import csv

def configWrite(pinA,pinB,loopTime,loop):
    with open('config.csv', 'w') as configfile:
        config = [pinA,pinB,loopTime,loop]
        configwriter = csv.writer(configfile)
        configwriter.writerow(config)
        configfile.close()

def configRead():
    config = [5,6,129,True]
    with open('config.csv') as configfile:
        configreader = csv.reader(configfile, delimiter=',')
        for row in configreader:
            if len(row)>3:
                for i in range(0,len(row)):
                    if row[i] == 'True':
                        config[i] = True
                    elif row[i] == 'False':
                        config[i] = False
                    else:
                        config[i]=int(row[i])

    return config

config = configRead()
# Setting up GPIO pins
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(config[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(config[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)

def csvRead():
    data = []
    with open('devices.csv', newline='') as devicefile:
        devicereader = csv.reader(devicefile)
        mylist = list(devicereader)
        for i in range(0,len(mylist)):
            if (mylist[i]!=[]):
                data.append(mylist[i])
    return data

def csvWrite(name,ip,mac):
    with open('devices.csv', 'a', newline='') as devicefile:
        device = [name,ip,mac]
        devicewriter = csv.writer(devicefile)
        devicewriter.writerow('')
        devicewriter.writerow(device)
        devicefile.close()

def csvDelete(name):
    lines = list()
    with open('devices.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == name:
                    lines.remove(row)

        list2 = [x for x in lines if x != []]
    if(os.path.exists('devices.csv') and os.path.isfile('devices.csv')):
        os.remove('devices.csv')

    with open('devices.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(list2)                   

def newPinConfig(newPinA,newPinB):
    config[0] = newPinA
    config[1] = newPinB

def gethostIP():
    local_ip=socket.gethostbyname(socket.gethostname())
    return local_ip

def WakeOnLan(MAC_address):
    send_magic_packet(MAC_address)

def pingTestAll(data):
    known_devices_IP = createListFromData(data,1)
    known_devices_STATUS = ['IS DOWN']*len(known_devices_IP)
    for i in range(0,4):
        known_devices_STATUS = pingTest(known_devices_IP,known_devices_STATUS)
        print()
        print('-----------------------------')
        print()
        print('----------------------------=')
        print()
    return known_devices_STATUS

def pingTest(known_devices_IP,known_devices_STATUS):
    for i in range(0,len(known_devices_IP)):
        response = os.system('ping -c 1 ' + known_devices_IP[i])
        if response == 0:
            known_devices_STATUS[i] = 'IS UP'
            print(known_devices_IP[i], 'is up')
        else:
            known_devices_STATUS[i] = 'IS DOWN'
            print(known_devices_IP[i],'is down')
    return known_devices_STATUS
		
def wol(known_devices_MAC):
    if len(known_devices_MAC) == 0:
        print ("\n*** No device given to power up\n")
    else:
        for i in range(0,len(known_devices_MAC)):
            WakeOnLan(known_devices_MAC[i])
            print('WOL sent to',known_devices_MAC[i])
            time.sleep(2)

def createListFromData(data,MACorIP):
    mylist = []
    for i in range(0,len(data)):
        mylist.append(data[i][MACorIP]) #get MAC
    return mylist


def run(data,returnTrue):
    # if(GPIO.input(config[0]) == 0 and GPIO.input(config[1]) == 0):
    print("Pin ",config[0]," is Low and Pin ",config[1]," is Low")
    known_devices_IP = createListFromData(data,1)
    known_devices_STATUS = ['IS DOWN']*len(known_devices_IP) #what happens if devices are up
    known_devices_MAC = createListFromData(data,2)   
    print('WAKE ON LAN running...')
    print('Known Devices')
    print(data)
    if len(known_devices_MAC) == 0:
        print("No known devices")
        return
    else:
        wol(known_devices_MAC)
        time.sleep(1)
        known_devices_STATUS = pingTestAll(data)
        if returnTrue == True:
            return known_devices_STATUS
                
                    
    # elif(GPIO.input(config[0]) == 0 and GPIO.input(config[1]) == 1):
    #     print("Pin ",config[0]," is Low and Pin ",config[1]," is High")
        
    # elif(GPIO.input(config[0]) == 1 and GPIO.input(config[1]) == 0):
    #     print("Pin ",config[0]," is High and Pin ",config[1]," is Low")
    # else:
    #     print("Pin ",config[0]," is High and Pin ",config[1]," is High")

