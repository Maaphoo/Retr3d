# E-Waste 3D Printer
In 2009, discarded TVs, computers, peripherals (including printers, scanners, fax machines) mice, keyboards, and cell phones totaled about 2.37 million short tons. Most of our e-waste ends up in landfills—mostly in the developing world—where toxic metals leach into the environment. This open source project aims to convert some of that e-waste into usable 3D printers. 
## Software
E-Waste 3D Printer uses python and FreeCAD to 3D model printable parts for the construction of more 3D printers. Through globalVars.py dimensions of procured e-waste are turned into customized 3D models. E-Waste 3D Printer's software depends on FreeCAD's python scripting API. FreeCAD can be found [here](http://www.freecadweb.org/wiki/index.php?title=Download "Download FreeCAD").
## Installation
After downloading the most recent release of E-Waste 3D Printer, three configurations must be made that are machine specific. After configuring each option, make sure to uncomment the line by removing the “#”. Moreover, make sure to use forward slashes like this / and not back slashes like this \ . 

1. Change the following line in makePrinter.py to locate the folder containing FreeCAD's "FreeCAD.so" or "FreeCAD.dll" file. 
```
sys.path.append("/Applications/FreeCAD.app/Contents/lib")
```
For Windows users it is in the .../FreeCAD 0.xx/bin or .../FreeCAD 0.xx/lib folder
For Mac users it is inside the FreeCAD.app file. Use "show package contents" to locate it. .../FreeCAD.app/Contents/lib
For Linux users (debian baesd) it is sys.path.append('/usr/lib/freecad/lib')


2. Next, change the following line in makePrinter.py to locate the folder containing the printer building scripts.
```
sys.path.append("/Path/To/ewaste3Dprinter")
```
3. Finally, change the output directory in globalVars.py. This is where your 3D files will be stored after they are generated.
```
printerDir = "/Path/To/Storage/"
```

## Tests
To begin creating a printer from the default options, open FreeCAD. Next, select “Macros ...” from the “Macro” menu. 
![Select "Macros ..."](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/picture1.png)
Next, select the folder where “makePrinter.py” is stored. 
![Select "makePrinter.py"](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/picture2.png)
Finally, select “makePrinter.py” for the available options. After that, hit “Execute” to create a printer.
![Hit "Execute"](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/picture3.png)
If everything was installed correctly, you should now have something that looks like this:
![printer](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/picture4.png)
Remember, it might take a while for your printer to be modeled. Please be patient. 
