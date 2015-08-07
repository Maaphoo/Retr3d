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


import sys
import FreeCAD, Part, Drawing
import FreeCAD as App
import FreeCAD# as #
import globalVars as gv
import datetime
import os

    
def create(part):
    App.ActiveDocument.addObject('Drawing::FeaturePage','Page')
    App.ActiveDocument.Page.Template = os.path.dirname(os.path.abspath(__file__))+'/A3_Landscape_ISO7200.svg'
    
    App.ActiveDocument.addObject('Drawing::FeatureViewPart','View')
    App.ActiveDocument.View.Source = part
    App.ActiveDocument.View.Direction = (0.0,0.0,1.0)
    App.ActiveDocument.View.Scale = 1.0
    App.ActiveDocument.View.X = 200
    App.ActiveDocument.View.Y = 148
    App.ActiveDocument.Page.addObject(App.ActiveDocument.View)
    App.ActiveDocument.View.Scale = 1.0
    App.ActiveDocument.recompute()

def setup(part,view):
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"
    #part: "printBedSupport"
    #subpart: App.ActiveDocument.Pocket001
    
    FreeCAD.open(printerDir+"Parts/"+part+".FCStd")
    App.setActiveDocument(part)
    view = eval('App.ActiveDocument.'+view)
    create(view)
    App.getDocument(part).save()
    App.closeDocument(part)