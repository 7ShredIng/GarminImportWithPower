import sys, os
import subprocess 
import glob
import ConfigParser

assert (sys.version_info.major < 3),"ERROR: currently python2.7 only!"

#os.system('mount -L GARMIN /mnt/GarminFenix3')

## Read configuration
def config():
    config = ConfigParser.ConfigParser()
    config.read(".config")
    GarminDeviceFolder  = ConfigSectionMap("Folders")['GarminDevActivities']
    ImportDir           = ConfigSectionMap("Folders")['ImportDir']
    VirtualPowerDir     = ConfigSectionMap("Folders")['ExportDir']
    FitToTcx            = ConfigSectionMap("Scripts")['FitToTcx']
    TcxVPower           = ConfigSectionMap("Scripts")['TcxVPower']


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

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def main():
    config()
    checkPaths()
    importFitFiles()
    convertFitToTcx()
    calculateVirtualPower()
    exportVPowerFiles()

if __name__ == "__main__":
    main()
