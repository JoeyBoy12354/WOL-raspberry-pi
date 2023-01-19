from cmath import pi
import PySimpleGUI as sg
import os.path
# import sys
# sys.path.insert(1, '/home/pi/Desktop/Johann_code')
import Functions_NoPins
import time

# First the window layout in 2 columns
data = Functions_NoPins.csvRead()
config = Functions_NoPins.configRead()
print('config = ',config)
oldtime = time.time()

names = []
status = ['UNKNOWN']*len(data)
for i in range(0,len(data)):
    names.append(data[i][0])



view_column = [
    [
        sg.Text("New Device Example:   Johann    10.0.0.99    29:70:01:DC:47:28"),

    ],
    [
        sg.Text("          [Name]"),
        sg.Text("                   "),
        sg.Text("[IP address]"),
        sg.Text("             "),
        sg.Text("[MAC address]"),

    ],
    [
        sg.In(size=(20, 1), enable_events=True, key="-NAME-"),
        sg.In(size=(20, 1), enable_events=True, key="-IP-"),
        sg.In(size=(20, 1), enable_events=True, key="-MAC-"),
        sg.Button('Add'),
    ],
    [
        sg.Text(size=(40,1), key='-OUTPUT-'),
    ],
    [
        sg.Button('Select'),
        sg.Button('Delete')
    ],
    [
        sg.Listbox(values=names, select_mode='extended', key='-DEVICESELECT-', size=(50, 6))
    ],
    [
        sg.Text("Name"),
        sg.Text(size=(40,1), key='-DEVICENAME-'),
    ],
    [
        sg.Text("IP Address"),
        sg.Text(size=(40,1), key='-DEVICEIP-'),
    ],
    [
        sg.Text("MAC Address"),
        sg.Text(size=(40,1), key='-DEVICEMAC-'),
    ],
    [
        sg.Text(size=(40,1), key='-DEVICESTATUS-'),
    ],
    
]

# For now will only show the name of the file that was chosen
config_column = [
    [
    sg.Text("Config Settings"),
    ],
    [
        sg.Text("GPIO pins"),
        sg.In(size=(5, 1), enable_events=True, key="-GP1-"),
        sg.In(size=(5, 1), enable_events=True, key="-GP2-"),
        sg.Text('PinA: '+(str(config[0])+' '+'PinB: '+str(config[1])), key='-GPtxt-'),
    ],
    [
        sg.Text("Loop Timer[s]"),
        sg.In(size=(5, 1), enable_events=True, key="-TIME-"),
        sg.Text(str(config[2])+' seconds', key='-TIMEtxt-'),
    ],
    [
        sg.Button('Set New Config')
    ],
    [
        sg.Button('Run/Stop Loop'),
        sg.Text(config[3], key='-LOOP-'),
    ],
    [
        sg.Text('      ')
    ],
    [
        sg.Text('      ')
    ],
    [
        sg.Button('Force Wake All')
    ],
    [
        sg.Button('Force Ping All')
    ],
    [
        sg.Text("Local IP:"+Functions_NoPins.gethostIP(), key='-LOCALIP-'),
    ]
    
]

# ----- Full layout -----
layout = [
    [
        sg.Column(view_column),
        sg.VSeperator(),
        sg.Column(config_column),
    ]
]


window = sg.Window("WOL -Johann Strydom", layout)

       
i = 0
# Run the Event Loop
while True:
    event, values = window.read(timeout=10)

    if i == 0:
        window['-LOOP-'].update('Running')
        if config[3] == False:
            window['-LOOP-'].update('Stopped')
        i=1

    if event == "Exit" or event == sg.WIN_CLOSED:
        running = False
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "Add":
        if len(values["-NAME-"])<1 :
            window['-OUTPUT-'].update('INCORRECT NAME')
        elif values["-NAME-"] in names:
            window['-OUTPUT-'].update('TWO DEVICES CANNOT HAVE THE SAME NAME')
        elif len(values["-IP-"])<len("0.0.0.0"):
            window['-OUTPUT-'].update('INCORRECT IP')
        elif len(values["-MAC-"])<len("00-00-00-00-00-00") :
            window['-OUTPUT-'].update('INCORRECT MAC')
        else:
            print('aNames(',len(names),') = ',names)
            print('aStatus(',len(status),') = ',status)
            print('aData(',len(data),') = ',data)

            Functions_NoPins.csvWrite(values["-NAME-"],values["-IP-"],values["-MAC-"])
            names.append(values["-NAME-"])
            data.append([values["-NAME-"],values["-IP-"],values["-MAC-"]])
            status.append('UNKNOWN')
            print('bNames(',len(names),') = ',names)
            print('bStatus(',len(status),') = ',status)
            print('bData(',len(data),') = ',data)

            if(len(names)!=len(status)):
                print("ERROR: amount of names and amount of device statuses do not agree")
                print("this can lead to devices being incorrectly identified as up")
                print("Possible debug: Delete all devices, restart program and then re-add")
            print('newName = ',names)
            print('newData = ',data)
            window['-OUTPUT-'].update('SUCCESSFULLY ADDED NEW DEVICE')
            window['-DEVICESELECT-'].update(values = names)
            print('cNames(',len(names),') = ',names)
            print('cStatus(',len(status),') = ',status)
            
    if event == "Select":
        data = Functions_NoPins.csvRead()
        for i in range(0,len(data)):
            if  values['-DEVICESELECT-'][0] == data[i][0]:
                window['-DEVICENAME-'].update(data[i][0])
                window['-DEVICEIP-'].update(data[i][1])
                window['-DEVICEMAC-'].update(data[i][2])
                window['-DEVICESTATUS-'].update(status[i])
            
    if event == "Delete":
        print('Delete Device Button Pressed')
        print('Delete ',values['-DEVICESELECT-'][0])
        index = names.index(values['-DEVICESELECT-'][0])
        status.remove(status[index])
        names.remove(names[index])
        Functions_NoPins.csvDelete(values['-DEVICESELECT-'][0])
        data  = Functions_NoPins.csvRead()

        print('dNames(',len(names),') = ',names)
        print('dStatus(',len(status),') = ',status)
        print('dData(',len(data),') = ',data)

        window['-DEVICESELECT-'].update(values = names)


        print('eNames(',len(names),') = ',names)
        print('eStatus(',len(status),') = ',status)

    if event == 'Force Start All':
        print('Force button pressed')
        status = Functions_NoPins.run(data,True)

    if event == 'Force Check Status':
        print("Force Check Status")
        status = Functions_NoPins.pingTestAll(data,True)

    if event == 'Set New Config':
        print('Set New Config')
        emptyCheckTime = values['-TIME-']
        emptyCheckGP1 = values['-GP1-']
        emptyCheckGP2 = values['-GP2-']

        if emptyCheckTime != '':
            if int(values['-TIME-']) <59:
                window['-OUTPUT-'].update('Time > 59 seconds')
                print('Time > 59 seconds')
            else:
                config[2] = int(values['-TIME-'])
        else:
            print('Time not set')

        if emptyCheckGP1 != '':
            config[0] = int(values['-GP1-'])
        else:
            print('PinA not set')

        if emptyCheckGP2 != '':
            config[1] = int(values['-GP2-'])
        else:
            print('PinB not set')

        if config[1]==config[0]:
            window['-OUTPUT-'].update('Pins cannot have the same value')
            print('WARNING: Pin A may not be equal to Pin B')


        #if int(values['-GP2-']) == int(values['-GP1-']):
        Functions_NoPins.configWrite(config[0],config[1],config[2],config[3])
        Functions_NoPins.newPinConfig(config[0],config[1])
        window['-GPtxt-'].update('PinA: '+(str(config[0])+' '+'PinB: '+str(config[1])))
        window['-TIMEtxt-'].update(str(config[2])+' seconds')


    #print("CHECK = ",time.time()-oldtime,'looptime = ', config[2])
    if time.time() - oldtime > config[2]:
        #print("timer check difference = ",time.time()-oldtime,'looptime = ', config[2])
        window['-LOCALIP-'].update("Local IP:"+Functions_NoPins.gethostIP())
        if config[3] == False:
            print('Loops Disabled.')
            oldtime = time.time()
        else:
            print('Loops Enabled. Set to run every ',config[2],' seconds')
            oldtime = time.time()
            status = Functions_NoPins.run(data,True)
    
    if event == 'Run/Stop Loop':
        print('Run/Stop Loops Button')
        if config[3] == True:
            config[3] = False
            window['-LOOP-'].update('Stopped')
            Functions_NoPins.configWrite(config[0],config[1],config[2],config[3])
            print('Loops Disabled')
        else:
            config[3] = True
            window['-LOOP-'].update('Running')
            Functions_NoPins.configWrite(config[0],config[1],config[2],config[3])
            print('Loops Enabled. Set to run every ',config[2],' seconds')

window.close()

