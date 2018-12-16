![Retr3d Logo](https://raw.githubusercontent.com/masterperson40/retr3d/develop/docs/retr3d.png)
Retr3d (ˈriːˌtred) is a framework dedicated to affordable 3D printing equipment for developing economies that can be locally sourced, locally maintained and locally improved.

We believe that 3D printing can be as transformative in developing countries as the mobile phone. As with the mobile phone, which has already changed the way people across the Africa communicate, introducing 3D printing at the community level offers the potential to localize manufacturing. Which is why we are making it possible to build Retr3d machines from the thousands of tonnes of e-waste which would otherwise end up as landfill.
## Software
Retr3d uses python and FreeCAD to 3D model printable parts for the construction of more 3D printers. Through globalVars.py dimensions of procured e-waste are turned into customized 3D models. Retr3d's software depends on FreeCAD's python scripting API. FreeCAD can be found [here](http://www.freecadweb.org/wiki/index.php?title=Download "Download FreeCAD").
## Installation: Quick Version
Head over to our [latest release](https://github.com/masterperson40/retr3d/releases/latest) and download your appropriate file. Next, extract it. Hazzah! You're all done, now head over to <a href="#getting-started">Getting Started</a> to get on your way.

## Configuration
All of the customizable options can be configured [here.](https://cdn.combinatronics.com/masterperson40/retr3d/master/config_generator/index.html) After generating your configuration file make sure to replace the original "globalVars.py file with the newly generated one.
## Getting Started
To begin creating a printer from the default options, open FreeCAD. Next, select from the menu.
![Select "Macro > Macros ..."](https://github.com/masterperson40/retr3d/raw/master/docs/step1.1.png)
<br />
Next, select the folder where is stored.
<br />
![Click the "..." Button](https://github.com/masterperson40/retr3d/raw/master/docs/step2.png)
Finally, select for the available options. After that, hit to create a printer.
![Click makePrinter.py](https://github.com/masterperson40/retr3d/raw/master/docs/step4.png)
<br />
If everything was installed correctly, you should now have something that looks like this:
![printer](https://github.com/masterperson40/retr3d/raw/master/docs/printer.png)
<br />
Remember, it might take a while for your printer to be modelled. Please be patient. 
## Plate
To facilitate an efficient work flow, Retr3d can interface with [Plater](https://github.com/RobotsWar/Plater) to arrange parts in an extremely efficient manner. Make sure to put the appropriate version of plater in the "plater" folder. (Eg. plater.exe, plater.app, or plater)


![Plater](https://github.com/masterperson40/retr3d/raw/master/docs/picture5.png)
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


