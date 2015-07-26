import os 
import datetime
import globalVars as gv
import shutil
import platform
import subprocess

def run(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def slic3r():
    #Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"
    
    #Name Variables
<<<<<<< HEAD
    sli3erName = gv.sli3erName
    if len(gv.sli3erVars)>1:
      sli3erVars = gv.sli3erVars.split( )
    else:
      sli3erVars = gv.sli3erVars
    
    #Go Time, Start Plater
    if not os.path.exists(printerDir+'GCode/'):
        os.makedirs(printerDir+'GCode/')
        
    if platform.system()=='Windows':
	for filename in os.listdir(printerDir+'STL_Files/'):
	    command = [os.path.dirname(os.path.abspath(__file__))+'/Slic3r/slic3r-console.exe', printerDir+'STL_Files/'+filename]
	    for line in run(command):
		print line.rstrip()
	
    if platform.system()=='Darwin':    #OSX 
	for filename in os.listdir(printerDir+'STL_Files/'):
	    command = [os.path.dirname(os.path.abspath(__file__))+'/Slic3r/bin/Slic3r.app/Contents/MacOS/slic3r', printerDir+'STL_Files/'+filename]
	    for line in run(command):
		print line.rstrip()
	
    if platform.system()=='Linux':
        for filename in os.listdir(printerDir+'STL_Files/'):
	    command = [os.path.dirname(os.path.abspath(__file__))+'/Slic3r/bin/slic3r', printerDir+'STL_Files/'+filename]
	    for line in run(command):
		print line.rstrip()
