from cmath import pi
import PySimpleGUI as sg
import os.path
import Functions 
import time

# First the window layout in 2 columns
data = Functions.csvRead()
config = Functions.configRead()
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
        sg.Text("Local IP:"+Functions.gethostIP(), key='-LOCALIP-'),
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
            Functions.csvWrite(values["-NAME-"],values["-IP-"],values["-MAC-"])
            names.append(values["-NAME-"])
            data.append([values["-NAME-"],values["-IP-"],values["-MAC-"]])
            status.append('UNKNOWN')
            if(len(names)!=len(status)):
                print("ERROR: amount of names and amount of device statuses do not agree")
                print("this can lead to devices being incorrectly identified as up")
                print("Possible debug: Delete all devices, restart program and then re-add")
            print('newName = ',names)
            print('newData = ',data)
            window['-OUTPUT-'].update('SUCCESSFULLY ADDED NEW DEVICE')
            window['-DEVICESELECT-'].update(values = names)
            
    if event == "Select":
        data = Functions.csvRead()
        for i in range(0,len(data)):
            if  values['-DEVICESELECT-'][0] == data[i][0]:
                window['-DEVICENAME-'].update(data[i][0])
                window['-DEVICEIP-'].update(data[i][1])
                window['-DEVICEMAC-'].update(data[i][2])
                window['-DEVICESTATUS-'].update(status[i])
            
    if event == "Delete":
        print('Delete Device Button Pressed')
        print('Delete ')
        index = names.index(values['-DEVICESELECT-'][0])
        status.remove(status[index])
        names.remove(names[index])
        Functions.csvDelete(values['-DEVICESELECT-'][0])
        window['-DEVICESELECT-'].update(values = names)
        data  = Functions.csvRead()

    if event == 'Force Wake All':
        print('Force Wake button pressed')
        status = Functions.run(data,True)

    if event == 'Force Ping All':
        print('Force Ping button pressed')
        status = Functions.pingTestAll(data)

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
        
        Functions.configWrite(config[0],config[1],config[2],config[3])
        Functions.newPinConfig(config[0],config[1])
        window['-GPtxt-'].update('PinA: '+(str(config[0])+' '+'PinB: '+str(config[1])))
        window['-TIMEtxt-'].update(str(config[2])+' seconds')


    if time.time() - oldtime > config[2]:
        window['-LOCALIP-'].update("Local IP:"+Functions.gethostIP())
        if config[3] == False:
            print('Loops Disabled.')
            oldtime = time.time()
        else:
            print('Loops Enabled. Set to run every ',config[2],' seconds')
            oldtime = time.time()
            status = Functions.run(data,True)
    
    if event == 'Run/Stop Loop':
        print('Run/Stop Loops Button')
        if config[3] == True:
            config[3] = False
            window['-LOOP-'].update('Stopped')
            Functions.configWrite(config[0],config[1],config[2],config[3])
            print('Loops Disabled')
        else:
            config[3] = True
            window['-LOOP-'].update('Running')
            Functions.configWrite(config[0],config[1],config[2],config[3])
            print('Loops Enabled. Set to run every ',config[2],' seconds')

window.close()

