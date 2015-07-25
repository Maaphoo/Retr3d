import os 
import datetime
import globalVars as gv
import shutil

def slic3r():
    #Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"
    
    #Name Variables
    slic3rName = gv.slic3rName
    slic3rVars = gv.slic3rVars

    #Go Time, Start Slic3r
    os.system('mkdir '+printerDir+'GCode/') 
#    if not os.path.exists(printerDir+'GCode/'):
#        os.makedirs(printerDir+'GCode/')

    #Slice all stl files
    os.system(os.path.abspath(os.path.join(os.path.dirname(__file__),"."))+'/Slic3r/'+slic3rName+' '+printerDir+'STL_Files/*.stl '+ slic3rVars +' --output '+printerDir+'GCode/')