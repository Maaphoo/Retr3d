# Copyright 2015 Michael Uttmark
# 
# This file is part of Retr3d.
# 
# Retr3d is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Retr3d is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Retr3d.  If not, see <http://www.gnu.org/licenses/>.

import os
import datetime
import globalVars as gv
import platform
import subprocess
import threading


def run(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def slic3(local_path):
    # Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerdir = gv.printerDir + "Printer_" + date + "/"
    slic3rVars = gv.slic3rVars.split()


    # Remove files that might have been left over by plater
    for filename in os.listdir(printerdir + 'STL_Files/'):
        if not ('.stl' in filename):
            os.remove(printerdir + 'STL_Files/' + filename)

    # Make GCode folder
    if not os.path.exists(printerdir + 'GCode/'):
        os.makedirs(printerdir + 'GCode/')

    # Run Slic3r
    if platform.system() == 'Windows':
        for filename in os.listdir(printerdir + 'STL_Files/'):
            command = [local_path + '/Slic3r/Slic3r-Windows/slic3r-console.exe', '--output', printerdir + 'GCode/',
                       printerdir + 'STL_Files/' + filename]
            command[1:1] = slic3rVars
            for line in run(command):
                print line.rstrip()

    if platform.system() == 'Darwin':  # OSX
        for filename in os.listdir(printerdir + 'STL_Files/'):
            command = [local_path + '/Slic3r/Slic3r-Mac.app/Contents/MacOS/slic3r',
                       '--output', printerdir + 'GCode/',
                       printerdir + 'STL_Files/' + filename]
            command[1:1] = slic3rVars
            for line in run(command):
                print line.rstrip()

    if platform.system() == 'Linux':
        for filename in os.listdir(printerdir + 'STL_Files/'):
            command = [local_path + '/Slic3r/Slic3r-Linux/bin/slic3r', '--output', printerdir + 'GCode/',
                       printerdir + 'STL_Files/' + filename]
            command[1:1] = slic3rVars
            for line in run(command):
                print line.rstrip()


def slic3r():
    local_path = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == 'Darwin':
        slic3(local_path)
    else: 
        threads = []
        t = threading.Thread(target=slic3, args=(local_path,))
        threads.append(t)
        t.start()
