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