import os 
import datetime
import globalVars as gv
import shutil

def slic3r():
    #Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"
    
    #Name Variables
    sli3erName = gv.sli3erName
    sli3erVars = gv.sli3erVars
    
    #Go Time, Start Plater
    os.system('mkdir '+printerDir+'GCode/')
    os.system(os.path.dirname(os.path.abspath(__file__))+'/Slic3r/bin/'+sli3erName +' '+printerDir+'STL_Files/*.stl '+ sli3erVars +' '+'--output '+printerDir+'GCode/')
