from ephem import *
import numpy as np
import pylab as plt
import glob, os
import inittasks as it
import plotutilities as plutil
import redpipe as pipe
import sys, getopt
import healpy as hp

class stripe():

      def __init__(self):
          pass

      def call_mk_map_mod(self):

          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")

             mk_file = it.PATH_CODE + "mk_map_mod.py"

             file_names = glob.glob("*G.fits")
          
             for file_name in file_names:
	         command = "python "+mk_file+" "+file_name+" -i -m "+file_name[:-6]+"_healpix.fits "+"--nside="+str(256)
                 print("CMD >>> "+command)
                 os.system(command)  
             os.chdir(it.PATH_CODE)

      def plot_healpix(file_name="zen.2457545.47315.xx.HH.uvcU_healpix.fits"):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             
             #file_names = glob.glob("*_healpix.fits") 

             haslam = hp.read_map(file_name)
             proj_map = hp.cartview(haslam,coord=['G','C'], max=2e5, xsize=2000,return_projected_map=True,title="Haslam 408 MHz with no filtering",cbar=False)
             hp.graticule()
             
if __name__ == "__main__":
   s = stripe()
   #s.call_mk_map_mod()
   plot_healpix()  
