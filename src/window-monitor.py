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

from gi.repository import Nautilus, GObject
import subprocess, os.path

class LocationMonitorExtension(GObject.GObject, Nautilus.LocationWidgetProvider):
    windows = []

    def get_widget(self, uri, window):
        # Skip initial setting
        if window in LocationMonitorExtension.windows:
            # Note: dbus must be called asynchronously otherwise it would deadlock from Nautilus trying to talk to itself.
            exe = os.path.expanduser("~/.local/share/nautilus-python/window-monitor-helper.py")
            process = subprocess.Popen(exe + ' >/dev/null 2>&1', shell=True)
        else:
            LocationMonitorExtension.windows.append(window)

        return None
