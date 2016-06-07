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

import subprocess, os.path

home = os.path.expanduser("~/")
user = home.strip('/').split('/')
user = user[-1]

# Copy the extension
extdir = home + '.local/share/nautilus-python/extensions/'
cmd = 'mkdir -p "%s"' % (extdir)
subprocess.call(cmd, shell=True)
cmd = 'cp window-monitor.py "%s"' % (extdir)
subprocess.call(cmd, shell=True)
cmd = 'chmod u+x "%swindow-monitor.py"' % (extdir)
subprocess.call(cmd, shell=True)

# Copy the helpers
npdir = home + '.local/share/nautilus-python/'
cmd = 'cp window-monitor-*.py "%s"' % (npdir)
subprocess.call(cmd, shell=True)
cmd = 'chmod u+x "%swindow-monitor-*.py"' % (npdir)
subprocess.call(cmd, shell=True)

# Create conf file
conf = home + ".config/nautilus-window-monitor.conf"
if not os.path.isfile(conf):
    file = open(conf, "w")
    file.write('file:///home/%s\t1079\t60\t840\t550\n' % (user))
    file.close()

# Create autostart file
desktop = home + '.config/autostart/nautilus-window-monitor.desktop'
file = open(desktop, "w")
file.write('[Desktop Entry]\n\
Type=Application\n\
Exec=/home/%s/.local/share/nautilus-python/window-monitor-login.py\n\
Hidden=false\n\
NoDisplay=false\n\
X-GNOME-Autostart-enabled=true\n\
Name=Nautilus Window Monitor\n\
Comment=Save Gnome Files (Nautilus) file manager window locations and folders.\n' % (user))
file.close()

print 'Installation completed'
