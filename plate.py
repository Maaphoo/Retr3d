import os 
import datetime
import globalVars as gv
import shutil
import subprocess
import platform

def plate():
    #Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"
    
    #Name Variables
    platerName = gv.platerName
    platerWidth = gv.platerWidth
    platerHeight = gv.platerHeight
    platerPrecision = gv.platerPrecision
    platerSpacing = gv.platerSpacing
    platerDelta = gv.platerDelta
    platerRotation = gv.platerRotation
    
    #Move Files to the Right Location
    shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater.conf', printerDir+'STL_Files/plater.conf')
    
    #Go Time, Start Plater
    if platform.system()=='Windows':
        shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater.exe', printerDir+'STL_Files/plater.exe')
	subprocess.check_output([printerDir+'STL_Files/plater.exe','-v', '-W '+ str(platerWidth), '-H '+str(platerHeight), '-j '+str(platerPrecision), '-s '+str(platerSpacing), '-d '+str(platerDelta), '-r '+str(platerRotation), printerDir+'STL_Files/plater.conf'])
	os.remove(printerDir+'STL_Files/plater.exe')
	
    if platform.system()=='Darwin':    #OSX 
        shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater-mac', printerDir+'STL_Files/plater-mac')
	subprocess.check_output([printerDir+'STL_Files/plater-mac','-v', '-W '+ str(platerWidth), '-H '+str(platerHeight), '-j '+str(platerPrecision), '-s '+str(platerSpacing), '-d '+str(platerDelta), '-r '+str(platerRotation), printerDir+'STL_Files/plater.conf'])
	os.remove(printerDir+'STL_Files/plater-mac') 
	
    if platform.system()=='Linux':
        shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater-linux', printerDir+'STL_Files/'+platerName)
        subprocess.check_output([printerDir+'STL_Files/plater-linux','-v', '-W '+ str(platerWidth), '-H '+str(platerHeight), '-j '+str(platerPrecision), '-s '+str(platerSpacing), '-d '+str(platerDelta), '-r '+str(platerRotation), printerDir+'STL_Files/plater.conf'])
        os.remove(printerDir+'STL_Files/plater-linux')
    
    #Clean up after our self
    os.remove(printerDir+'STL_Files/plater.conf')  