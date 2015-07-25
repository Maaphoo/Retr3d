import os 
import datetime
import globalVars as gv
import shutil

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
    shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/'+platerName, printerDir+'STL_Files/'+platerName)
    shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater.conf', printerDir+'STL_Files/plater.conf')
    
    #Go Time, Start Plater
    os.system(printerDir+'STL_Files/'+platerName+' -v -W '+str(platerWidth)+' '+' -H '+str(platerHeight)+' -j '+str(platerPrecision)+' -s '+str(platerSpacing)+' -d '+str(platerDelta)+' -r '+str(platerRotation)+' '+printerDir+'STL_Files/plater.conf')
    
    #Clean up after our self
    os.remove(printerDir+'STL_Files/'+platerName)
    os.remove(printerDir+'STL_Files/plater.conf')
