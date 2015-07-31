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
            command = [local_path + '/Slic3r/slic3r-console.exe', '--output', printerdir + 'GCode/',
                       printerdir + 'STL_Files/' + filename]
            for line in run(command):
                print line.rstrip()

    if platform.system() == 'Darwin':  # OSX
        for filename in os.listdir(printerdir + 'STL_Files/'):
            command = [local_path + '/Slic3r/Slic3r-Mac.app/Contents/MacOS/slic3r', '--output', printerdir + 'GCode/',
                       printerdir + 'STL_Files/' + filename]
            for line in run(command):
                print line.rstrip()

    if platform.system() == 'Linux':
        for filename in os.listdir(printerdir + 'STL_Files/'):
            command = [local_path + '/Slic3r/bin/slic3r', '--output', printerdir + 'GCode/',
                       printerdir + 'STL_Files/' + filename]
            for line in run(command):
                print line.rstrip()


def slic3r():
    local_path = os.path.dirname(os.path.abspath(__file__))
    threads = []
    t = threading.Thread(target=slic3, args=(local_path,))
    threads.append(t)
    t.start()
