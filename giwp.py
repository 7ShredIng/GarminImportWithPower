import sys, os
import subprocess 

assert (sys.version_info.major < 3),"ERROR: currently python2.7 only!"

GarminDeviceFolder = "/media/sick/GARMIN/GARMIN/ACTIVITY"
ImportDir = "/media/sick/Training/FenixImport/tcx"
VirtualPowerDir = "/media/sick/Training/FenixImport/vpower"

print("-- check if directories are available")
#assert (os.path.isdir(GarminDeviceFolder)),"ERROR: dir does not exist"
assert (os.path.isdir(ImportDir)),"ERROR: dir does not exist"
assert (os.path.isdir(VirtualPowerDir)),"ERROR: dir does not exist"

print("-- sync fit files to ImportDir")
importCommand = '/usr/bin/rsync --progress -r -v -s %s %s' % (GarminDeviceFolder, ImportDir)
p = subprocess.Popen(importCommand, shell=True).wait()

print("-- convert fit files to tcx")

print("-- calculate and add virtual power to tcx files")

print("-- sync vpower files to Golden Cheetah import directory")

print("-- import to Golden Cheetah")



