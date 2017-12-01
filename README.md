# GIWP
Sync FIT files from a Garmin device (e.g. Garmin Fenix), convert them to TCX files and add a calculated virtual power. These can be imported for further analysis in other tools e.g. Golden Cheetah.

# Dependencies
## FIT-to-TCX
### Dependencies
#### python-fitparse
A library to parse FIT files by David Cooper. https://github.com/dtcooper/python-fitparse
#### python-lxml 
A library to read and write XML files. 'apt-get install python-lxml'
### Install
Run 'sudo python setup.py install'.

## TCX VPower
Download from https://sourceforge.net/p/tcxvpower and extract.

## todo
Use gnu parallels for parallel processing.

# Configuration
In the .config file define the folders for processing the tcx files and the location of the used batch processing scripts.

[Folders]
GarminDevActivities: ""
ImportDir: ""
ExportDir: ""

[Scripts]
FitToTcx: ""
TcxVPower: ""
