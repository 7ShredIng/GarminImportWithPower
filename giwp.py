import sys, os
import subprocess 
import glob
import yaml 
from bunch import bunchify

assert (sys.version_info.major < 3),"ERROR: currently python2.7 only!"

#os.system('mount -L GARMIN /mnt/GarminFenix3')
#class Configuration(yaml.YAMLObject):
#    yaml_tag = '!Folders'
#
#    def __init__(self, name):
#        self.GarminDevActivities = GarminDevActivities
#        self.ImportDir = ImportDir
#        self.ExportDir = ExportDir
#        self.FitToTcx = FitToTcx
#        self.TcxPower= TcxPower

## Read configuration
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
