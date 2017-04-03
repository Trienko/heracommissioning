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

      def add_uv_tracks(self):
          os.chdir(PATH_DATA)
           
          for file in glob.glob("*.uvc"):
              command = "python " + PATH_TO_ADD_UVWS + " -C " + CAL_FILE +" "+ file
              print("CMD >>> "+command)
              os.system(command)

	  os.chdir(PATH_CODE)
                    

if __name__ == "__main__":
   inittasks_object = inittasks()
   inittasks_object.add_uv_tracks()
