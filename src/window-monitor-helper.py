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
from time import sleep
from Xlib.display import Display


# Get window position
def getPos(windid):
    wnd = dpy.create_resource_object('window', windid)
    geom = wnd.get_geometry()
    x = geom.x
    y = geom.y
    width = geom.width
    height = geom.height
    
    # Iterate to the top window
    tree = wnd.query_tree()
    while tree.parent.id != tree.root.id:
        wnd = tree.parent
        geom = wnd.get_geometry()
        x += geom.x
        y += geom.y
        tree = wnd.query_tree()

    return {'x': x, 'y': y, 'width': width, 'height': height}

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
        attr = getPos(windid)
        string = '%s\t%d\t%d\t%d\t%d\n' %(folders[0], attr['x'], attr['y'], attr['width'], attr['height'])
        file.write(string)

    file.close()
    return False

# Give nautilus time to change directories
sleep(2)
dpy = Display()
saveLocs()

