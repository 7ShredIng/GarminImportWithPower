import sys, os
import subprocess 
import glob
import yaml 
from bunch import bunchify

assert (sys.version_info.major < 3),"ERROR: currently python2.7 only!"

class GIWP:

    GarminDeviceFolder = ""
    ImportDir = ""
    VirtualPowerDir = ""
    FitToTcx = ""
    TcxVPower = ""

    #os.system('mount -L GARMIN /mnt/GarminFenix3')

    ## Read configuration from yaml.
    ## [Folders]
    ## - path to Garmin device where the FIT files are located
    ## - Import directory to where the files are processed
    ## - Export directory to where copy the virtual power files
    ## [Scripts]
    ## - batch script: fit to tcx conversion
    ## - batch script: vpower conversion
    def readConfig(self):
        with open('.config') as conf:
            configuration = yaml.safe_load(conf)
        
        b = bunchify(configuration)
        GIWP.GarminDeviceFolder  = b.Folders.GarminDevActivities
        GIWP.ImportDir           = b.Folders.ImportDir
        GIWP.VirtualPowerDir     = b.Folders.ExportDir
        GIWP.FitToTcx            = b.Scripts.FitToTcx
        GIWP.TcxVPower           = b.Scripts.TcxVPower
        conf.close()

    def checkPaths(self):
        print("-- check if directories are available")
        assert (os.path.isdir(GIWP.GarminDeviceFolder)),"ERROR: dir does not exist"
        assert (os.path.isdir(GIWP.ImportDir)),"ERROR: dir does not exist"
        assert (os.path.isdir(GIWP.VirtualPowerDir)),"ERROR: dir does not exist"

    def importFitFiles(self):
        print("-- sync fit files to ImportDir")
        importCommand = '/usr/bin/rsync --progress -rvsh --ignore-existing --remove-source-files %s %s' % (GIWP.GarminDeviceFolder, GIWP.ImportDir)
        p = subprocess.Popen(importCommand, shell=True).wait()

    def convertFitToTcx(self):
        print("-- convert fit files to tcx")
        convertFitToTcxCommand = '%s %s*.FIT' % (GIWP.FitToTcx, GIWP.ImportDir)
        print('%s' % convertFitToTcxCommand)
        p = subprocess.Popen(convertFitToTcxCommand, shell=True).wait()

    def calculateVirtualPower(self):
        print("-- calculate and add virtual power to tcx files")
        addVPowerCommand = '%s %s*.tcx' % (GIWP.TcxVPower, GIWP.ImportDir)
        print('%s' % addVPowerCommand)
        p = subprocess.Popen(addVPowerCommand, shell=True).wait()

    def exportVPowerFiles(self):
        print("-- sync vpower files to Golden Cheetah import directory")
        exportGCFolderCommand = '/usr/bin/rsync --progress -rvsh --include=\'vpower_*\' --include=\'*/\' --exclude=\'*\' %s %s' % (GIWP.ImportDir, GIWP.VirtualPowerDir)
        print('%s' % exportGCFolderCommand)
        p = subprocess.Popen(exportGCFolderCommand, shell=True).wait()

    def cleanup(self):
        print("-- delete unused files from tcx folder")
        for f in glob.glob(GIWP.ImportDir + "vpower*.tcx"):
            print(f)
            os.remove(f)
        for f in glob.glob(GIWP.ImportDir + "*.FIT.tcx"):
            print(f)
            os.remove(f)

def main():
    giwp = GIWP()
    giwp.readConfig()
    giwp.checkPaths()
    giwp.importFitFiles()
    giwp.convertFitToTcx()
    giwp.calculateVirtualPower()
    giwp.exportVPowerFiles()
    giwp.cleanup()

if __name__ == "__main__":
    main()
