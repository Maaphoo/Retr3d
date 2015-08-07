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
import shutil
import subprocess
import platform
import utilityFunctions as uf

source = os.path.basename(__file__)

def plate():
    #Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"
    
    #Plater Variables
    platerWidth = gv.platerWidth
    platerHeight = gv.platerHeight
    platerPrecision = gv.platerPrecision
    platerSpacing = gv.platerSpacing
    platerDelta = gv.platerDelta
    platerRotation = gv.platerRotation
    
    #Check platerRotation for low value
    minPlaterRotation = 20
    if platerRotation <= minPlaterRotation:
        uf.warning("Plater can take a long time to finish with Rotation values under " + str(minPlaterRotation)+".",
                   "Low platerRotation value. platerRotation = "+str(platerRotation),
                   gv.level, source)
    
    #Move Files to the Right Location
    shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater.conf', printerDir+'STL_Files/plater.conf')
    
    #Go Time, Start Plater
    if platform.system()=='Windows':
        shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater-win.exe', printerDir+'STL_Files/plater-win.exe')
        subprocess.check_output([printerDir+'STL_Files/plater-win.exe','-v', '-W '+ str(platerWidth), '-H '+str(platerHeight), '-j '+str(platerPrecision), '-s '+str(platerSpacing), '-d '+str(platerDelta), '-r '+str(platerRotation), printerDir+'STL_Files/plater.conf'])
        os.remove(printerDir+'STL_Files/plater-win.exe')

    if platform.system()=='Darwin':    #OSX 
        shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater-mac', printerDir+'STL_Files/plater-mac')
        subprocess.check_output([printerDir+'STL_Files/plater-mac','-v', '-W '+ str(platerWidth), '-H '+str(platerHeight), '-j '+str(platerPrecision), '-s '+str(platerSpacing), '-d '+str(platerDelta), '-r '+str(platerRotation), printerDir+'STL_Files/plater.conf'])
        os.remove(printerDir+'STL_Files/plater-mac') 

    if platform.system()=='Linux':
        shutil.copy2(os.path.dirname(os.path.abspath(__file__))+'/plater/plater-linux', printerDir+'STL_Files/plater-linux')
        subprocess.check_output([printerDir+'STL_Files/plater-linux','-v', '-W '+ str(platerWidth), '-H '+str(platerHeight), '-j '+str(platerPrecision), '-s '+str(platerSpacing), '-d '+str(platerDelta), '-r '+str(platerRotation), printerDir+'STL_Files/plater.conf'])
        os.remove(printerDir+'STL_Files/plater-linux')
    
    #Clean up after our self
    os.remove(printerDir+'STL_Files/plater.conf')  