import numpy as np
import pylab as plt
import glob, os

PATH_TO_ADD_UVWS = "/home/trienko/HERA/software/capo/dcj/scripts/add_uvws.py"
CAL_FILE = "hsa7458_v000_HH" 
PATH_TO_MIR_TO_FITS = "/usr/local/bin/miriad_to_uvfits.py"
PATH_DATA = "/home/trienko/HERA/conference/data/"
PATH_CODE = "/home/trienko/HERA/conference/code/"

class inittasks():

      def __init__(self):
          pass

      ##############################
      #Reading all files with the .uvc extension and running the add_uvws command to add uv_tracks to the miriad files
      ##############################
      def add_uv_tracks(self):
          os.chdir(PATH_DATA)
           
          for file in glob.glob("*.uvc"):
              command = "python " + PATH_TO_ADD_UVWS + " -C " + CAL_FILE +" "+ file
              print("CMD >>> "+command)
              os.system(command)

	  os.chdir(PATH_CODE)

      ##############################
      #Deleting the uvcU files (miriad files with uv-tracks added)
      ##############################
      def remove_uvcU(self):
          os.chdir(PATH_DATA)
          for file in glob.glob("*.uvcU"):
              command = "rm -r "+ file
              print("CMD >>> "+command)
              os.system(command)
          os.chdir(PATH_CODE)

      ##############################
      #converting uvcU files to uvfits (to run must be in sudo)
      ##############################
      def miriad_to_uvfits(self):
          os.chdir(PATH_DATA)
           
          for file in glob.glob("*.uvcU"):
              command = "python " + PATH_TO_MIR_TO_FITS +" "+ file
              print("CMD >>> "+command)
              os.system(command)

	  os.chdir(PATH_CODE)

      ##############################
      #Deleting the uvfits files
      ##############################
      def remove_uvfits(self):
          os.chdir(PATH_DATA)
          for file in glob.glob("*.uvfits"):
              command = "rm -r "+ file
              print("CMD >>> "+command)
              os.system(command)
          os.chdir(PATH_CODE)


if __name__ == "__main__":
   inittasks_object = inittasks()
   #inittasks_object.add_uv_tracks()
   inittasks_object.miriad_to_uvfits()
 

   #inittasks_object.remove_uvcU()

