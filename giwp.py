import sys, os
import subprocess 
import glob
import yaml 
from bunch import bunchify

assert (sys.version_info.major < 3),"ERROR: currently python2.7 only!"

#os.system('mount -L GARMIN /mnt/GarminFenix3')

## Read configuration from yaml.
## [Folders]
## - path to Garmin device where the FIT files are located
## - Import directory to where the files are processed
## - Export directory to where copy the virtual power files
## [Scripts]
## - batch script: fit to tcx conversion
## - batch script: vpower conversion
def readConfig():
    with open('.config') as conf:
        configuration = yaml.safe_load(conf)
    
    b = bunchify(configuration)
    GarminDeviceFolder  = b.Folders.GarminDevActivities
    ImportDir           = b.Folders.ImportDir
    VirtualPowerDir     = b.Folders.ExportDir
    FitToTcx            = b.Scripts.FitToTcx
    TcxVPower           = b.Scripts.TcxVPower
    conf.close()

def checkPaths():
    print("-- check if directories are available")
    assert (os.path.isdir(GarminDeviceFolder)),"ERROR: dir does not exist"
    assert (os.path.isdir(ImportDir)),"ERROR: dir does not exist"
    assert (os.path.isdir(VirtualPowerDir)),"ERROR: dir does not exist"

def importFitFiles():
    print("-- sync fit files to ImportDir")
    importCommand = '/usr/bin/rsync --progress -rvsh --ignore-existing %s %s' % (GarminDeviceFolder, ImportDir)
    p = subprocess.Popen(importCommand, shell=True).wait()

def convertFitToTcx():
    print("-- convert fit files to tcx")
    convertFitToTcxCommand = '%s %s*.FIT' % (FitToTcx, ImportDir)
    print('%s' % convertFitToTcxCommand)
    p = subprocess.Popen(convertFitToTcxCommand, shell=True).wait()

def calculateVirtualPower():
    print("-- calculate and add virtual power to tcx files")
    addVPowerCommand = '%s %s*.tcx' % (TcxVPower, ImportDir)
    print('%s' % addVPowerCommand)
    p = subprocess.Popen(addVPowerCommand, shell=True).wait()

def exportVPowerFiles():
    print("-- sync vpower files to Golden Cheetah import directory")
    exportGCFolderCommand = '/usr/bin/rsync --progress -rvsh --include=\'vpower_*\' --include=\'*/\' --exclude=\'*\' %s %s' % (ImportDir, VirtualPowerDir)
    for f in glob.glob(ImportDir + "vpower*.tcx"):
        os.remove(f)
    print('%s' % exportGCFolderCommand)
    p = subprocess.Popen(exportGCFolderCommand, shell=True).wait()

def main():
    readConfig()
    checkPaths()
    importFitFiles()
    convertFitToTcx()
    calculateVirtualPower()
    exportVPowerFiles()

if __name__ == "__main__":
    main()
