import datetime
import globalVars as gv
import shutil

def zipup():
    #Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"
    
    zipName = gv.zipName
    shutil.make_archive(printerDir+zipName, 'zip', printerDir+'STL_Files/')