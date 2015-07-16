# E-Waste 3D Printer
In 2009, discarded TVs, computers, peripherals (including printers, scanners, fax machines) mice, keyboards, and cell phones totaled about 2.37 million short tons. Most of our e-waste ends up in landfills—mostly in the developing world—where toxic metals leach into the environment. This open source project aims to convert some of that e-waste into usable 3D printers. 
## Software
E-Waste 3D Printer uses python and FreeCAD to 3D model printable parts for the construction of more 3D printers. Through globalVars.py dimensions of procured e-waste are turned into customized 3D models. E-Waste 3D Printer's software depends on FreeCAD's python scripting API. FreeCAD can be found [here](http://www.freecadweb.org/wiki/index.php?title=Download "Download FreeCAD").
## Configuration
All of the customisable options can be configured [here.](https://cdn.rawgit.com/masterperson40/ewaste3Dprinter/master/config_generator/index.html) After generating your configuration file make sure to replace the original "globalVars.py file with the newly generated one.
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
## Plate
To facilitate an efficient workflow, E-Waste 3D Printer can interface with [Plater](https://github.com/RobotsWar/Plater) to arrange parts in an extremely efficient manner. Make sure to put the appropriate version of plater in the "plater" folder. (Eg. plater.exe, plater.dmg, or plater)
![Plater](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/picture5.png)\
## Slic3r Integration
E-Waste 3D Printer can also interface with [Slic3r](https://github.com/alexrj/Slic3r) to slice parts automatically. After installing the dependencies, make sure to put the appropriate version of Slic3r in the "Slic3r" folder. (Eg. slic3r.exe, slic3r.dmg, or slic3r)