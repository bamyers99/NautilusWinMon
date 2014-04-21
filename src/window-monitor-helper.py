#!/usr/bin/env python2

"""
Save Gnome Files (Nautilus) file manager window locations and folders.

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

import dbus, re, os.path
from subprocess import check_output
from time import sleep

# Get nautilus window info 
def getLocs():
    locs = {}
    # dbus-send --print-reply --dest=org.freedesktop.FileManager1 /org/freedesktop/FileManager1 org.freedesktop.DBus.Properties.Get string:'org.freedesktop.FileManager1' string:'XUbuntuOpenLocationsXids'

    try:
        bus = dbus.SessionBus()
        fm = bus.get_object('org.freedesktop.FileManager1',
            '/org/freedesktop/FileManager1')
        locs = fm.Get('org.freedesktop.FileManager1',
            'XUbuntuOpenLocationsXids',
            dbus_interface='org.freedesktop.DBus.Properties')
    except dbus.DBusException as e:
        print 'dbus.DBusException: %s' % (e)
    
    return locs
    
    
# Save location/geometry
def saveLocs():
    locs = getLocs()
    if len(locs) == 0:
        return

    file = open(os.path.expanduser("~/.config/nautilus-window-monitor.conf"), "w")

    for windid, folders in locs.items():
        #print windid, '=', folders[0]
        Xwininfo = \
            check_output("xwininfo -frame -id %s" %windid, shell=True)
        match = re.search(r'Absolute upper-left X:\s*(\d+)', Xwininfo)
        wx = match.group(1)
        match = re.search(r'Absolute upper-left Y:\s*(\d+)', Xwininfo)
        wy = match.group(1)
        match = re.search(r'Width:\s*(\d+)', Xwininfo)
        ww = match.group(1)
        match = re.search(r'Height:\s*(\d+)', Xwininfo)
        wh = match.group(1)
        string = '%s\t%s\t%s\t%s\t%s\n' %(folders[0], wx, wy, ww, wh)
        file.write(string)

    file.close()
    return False

# Give nautilus time to change directories
sleep(2)
saveLocs()

