## Notice
E-Waste 3D Printer is now **Retr3d**, pronounced just like "Retread." This change reflects the "Retreading" of 2D printers with a Z-Axis.
_____________

# Retr3d
In 2009, discarded TVs, computers, peripherals (including printers, scanners, fax machines) mice, keyboards, and cell phones totaled about 2.37 million short tons. Most of our e-waste ends up in landfills where toxic metals leach into the environment. This open source project aims to convert some of that e-waste into usable 3D printers. 
## Software
Retr3d uses python and FreeCAD to 3D model printable parts for the construction of more 3D printers. Through globalVars.py dimensions of procured e-waste are turned into customized 3D models. Retr3d's software depends on FreeCAD's python scripting API. FreeCAD can be found [here](http://www.freecadweb.org/wiki/index.php?title=Download "Download FreeCAD").
## Installation: Quick Version
Head over to our [latest release](https://github.com/masterperson40/retr3d/releases/latest) and download your appropriate file. Next, extract it. Hazzah! You're all done, now head over to <a href="#Getting_Started">Getting Started</a> to get on your way.

## Configuration
All of the customizable options can be configured [here.](https://cdn.rawgit.com/masterperson40/ewaste3Dprinter/master/config_generator/index.html) After generating your configuration file make sure to replace the original "globalVars.py file with the newly generated one.
## Getting Started
To begin creating a printer from the default options, open FreeCAD. Next, select from the menu.
![Select "Macro > Macros ..."](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/step1.1.png)
<br />
Next, select the folder where is stored.
<br />
![Click the "..." Button](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/step2.png)
Finally, select for the available options. After that, hit to create a printer.
![Click makePrinter.py](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/step4.png)
<br />
If everything was installed correctly, you should now have something that looks like this:
![printer](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/printer.png)
<br />
Remember, it might take a while for your printer to be modelled. Please be patient. 
## Plate
To facilitate an efficient work flow, Retr3d can interface with [Plater](https://github.com/RobotsWar/Plater) to arrange parts in an extremely efficient manner. Make sure to put the appropriate version of plater in the "plater" folder. (Eg. plater.exe, plater.app, or plater)


![Plater](https://github.com/masterperson40/ewaste3Dprinter/raw/master/docs/picture5.png)
## Slic3r Integration
Retr3d can also interface with [Slic3r](https://github.com/alexrj/Slic3r) to slice parts automatically. After installing the dependencies, make sure to put the appropriate version of Slic3r in the "Slic3r" folder. (Eg. slic3r.exe, slic3r.app, or slic3r)

## Troubleshooting
#### AttributeError: 'module' object has no attribute 'getDocument'
This error is generated when running "makePrinter.py" directly from the command line. To fix, follow the instructions under "Getting Started" to run "makePrinter.py" as a FreeCAD macro.

#### raise Exception("getFace() error: No such face exists.")

Due to the way FreeCAD assigns faces in it's version 0.15, some users may have to downgrade to an earlier version. FreeCAD 0.14 Revision 2935 has been confirmed to work on a multitude of operating systems. Also, FreeCAD Version 0.16 Revision 5239 has also been confirmed to work.

To downgrade on Debian Linux:
```
sudo apt-get install freecad=0.13.2935-dfsg-1.1build1
```


