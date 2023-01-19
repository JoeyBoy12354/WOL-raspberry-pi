
import sys, struct, socket
import RPi.GPIO as GPIO
import time
from wakeonlan import send_magic_packet
import os
import csv

# Configuration variables
broadcast = ['10.127.181.255']
wol_port = 9
startWOL = True
pinA = 5
pinB = 6
# Setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def csvWrite(name,ip,mac):
    with open('devices.csv', 'a', newline='') as devicefile:
        device = [name,ip,mac]
        devicewriter = csv.writer(devicefile)
        devicewriter.writerow('')
        devicewriter.writerow(device)
        devicefile.close()

def csvRead():
    data = []
    with open('devices.csv', newline='') as devicefile:
        devicereader = csv.reader(devicefile)
        mylist = list(devicereader)
        for i in range(0,len(mylist)):
            if (mylist[i]!=[]):
                data.append(mylist[i])
    return data

def csvDelete(name):
    with open('devices.csv', 'rb') as devicefile:
        devicewriter = csv.writer(devicefile)
        counter = 0
        for row in csv.reader(devicefile):
            for i in range(0,len(name)):
                if row[0] == name[0]:
                    counter = counter+1
            if counter == len(name):
                devicewriter.writerow(row)
                counter = 0
                return
            else:
                counter = 0       

def newConfig(newPinA,newPinB):
    pinA = newPinA
    pinB = newPinB

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

def run(data):
    if(GPIO.input(5) == 0 and GPIO.input(6) == 0 and startWOL == True):
        known_devices_IP = createListFromData(data,1)
        known_devices_STATUS = ['IS DOWN']*len(known_devices_IP)
        known_devices_MAC = createListFromData(data,2)   
        if (startWOL == True):
            print('WAKE ON LAN running...')
            print('Known Devices')
            print(data)
            if len(known_devices_MAC) == 0:
                print("No known devices")
                return
            else:
                startWOL = False
                wol(known_devices_MAC)
                time.sleep(10)
                known_devices_STATUS = pingTestAll(data)
                return known_devices_STATUS
    elif(GPIO.input(5) == 0 and GPIO.input(6) == 1):
        print("Pin 6 is High and Pin 5 is Low")
        startWOL = True
        
    elif(GPIO.input(5) == 1 and GPIO.input(6) == 0):
        print("Pin 5 is High and Pin 6 is Low")
        startWOL = True
    else:
        print("Both Pins are High")
        startWOL = True
# while True:
# 	time.sleep(10)
# 	check()
