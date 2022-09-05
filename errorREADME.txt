4 September
---------------BUGS--------------------
Both Pins or neither must be allocated new values when setting new config.
Otherwise crash
File "C:\Johann\Raspberry Pi\Pi code exe\UI_NoPins.py", line 202, in <module>
    if int(values['-GP1-']) == int(values['-GP2-']):
ValueError: invalid literal for int() with base 10: ''

When adding new devices sometimes program crashes.
In UI.py line 144
status.append('UNKNOWN')
AttributeError: 'Nonetype' object has no attribute append

-------------FEATURES------------------
It is now not possible to add two devices that have the same name

---------------FIXES-------------------
Bug from both pins not being able to allocate a value to only 1 pin has been fixed.

Bug where length of status array does not match length of name array has been fixed.









5 August


---------------BUGS--------------------
01:04 video - Albert *FIXED
Device not deleted when selected then delete pressed
'Loops Disabled' printing much faster than time allocated
then
Run/Stop loops button pressed
'Loops Enabled. Set to run' is printed twice
Then error at @ line 147 print("Pin "+config[0]+"is High and...... is Low")
    TypeError: can only concatenate str (not "int") to str

00:23 & 01:07 video - Albert *FIXED
1 pin was high one was low
On boot
Run/Stop Loops button pressed
Loops Disabled
Run/Stop Loops button pressed
'Loops Enabled. Set to run' is printed twice
Then error @ line 144 print("Pin "+config[0]+"is High and...... is Low")
    TypeError: can only concatenate str (not "int") to str

00:36 video - Albert *COULD NOT RECREATE
After deleting devices
Then restart program
Device A still showed up on list
Upon selection of device A program shutdown

00:28 video - Albert *COULD NOT RECREATE
After deleting 3 devices (proof is shown with 'Delete' in console 3 times)
Device A, JohannNew and HPServer still showed up on list


--------------CONFIRMATIONS--------------
00:25 video - Albert
Both pins set to high by switch then WOL was sent and pings 

00:57 video - Albert
Loop can be stopped
Config info (pins and timer) can be changed 
Set config clicked successfully change config
Loop enabled then successfully running


--------------FEATURES--------------------
00:57 & 01:44 video - Albert
Allow pin config to be changed without having to also change loop timer


--------------FIXES----------------------
Bug from 01:04 video - Albert
Loop Disabled now only prints when loop timer has completed one full loop
Loop Disabled printing very frequently has been fixed

Bug from 01:04 & 00:23 & 01:07 video - Albert
lines with print("Pin "+config[0]+" is xxxx and Pin "+config[1]+" is xxxx")
replaced with
print("Pin ",config[0]," is xxxx and Pin ",config[1]," is xxxx")
Concatenation error has been fixed

Bug from 00:36 & 00:28 video - Albert
Changed how files are imported from using sys.path.insert(1, '/home/pi/Desktop/Johann_code')
Now just import Functions

Changed how csv files are opened from
with open('/home/pi/Desktop/Johann_code/devices.csv', newline='') as devicefile:
to
with open('devices.csv', newline='') as devicefile:
same for config.csv

Bug: Delete button not deleting items from devices.csv file
**Bug could not be recreated and this fix may or may not work

Feature 00:57 & 01:44 video - Albert
Allow pin config to be changed without having to also change loop timer
Feature has been added with new console prints and app output messages