#!/usr/bin/env python2

"""
Restore Gnome Files (Nautilus) file manager window locations and folders.

Author: Bruce Myers (http://brucemyers.com/)

Copyright 2014 Myers Enterprises II

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import dbus, re, os.path, subprocess
from time import sleep

# Read the saved windows
try:
    file = open(os.path.expanduser("~/.config/location-monitor"), "r")
except IOError:
    exit(0)
    
lines = file.readlines()
file.close()

if len(lines) == 0:
    exit(0)

winds = {}

# Start up the nautilus windows
for line in lines:
    args = line.strip().split('\t')
    winds[args[0]] = (args[1], args[2], args[3], args[4])
    # Note: The geometry parameter does not work because the windows open too fast.
    cmd = "nautilus " + args[0]
    subprocess.call(cmd, shell=True)

# Wait for the windows to open
for x in range(10):
    #print 'Wait count: ', x
    bus = dbus.SessionBus()
    fm = bus.get_object('org.freedesktop.FileManager1',
        '/org/freedesktop/FileManager1')
    locs = fm.Get('org.freedesktop.FileManager1', 'XUbuntuOpenLocationsXids',
        dbus_interface='org.freedesktop.DBus.Properties')
        
    if len(locs) == len(lines):
        break
        
    sleep(1)

# Position the windows
for windid, folders in locs.items():
    args = winds[folders[0]]
    #wmctrl -ir <WIN> -e '0,<X>,<Y>,<W>,<H>'
    cmd = "wmctrl -ir %s -e '0,%s,%s,%s,%s'" % (windid, args[0], args[1], args[2], args[3])
    #print cmd 
    subprocess.call(cmd, shell=True)

