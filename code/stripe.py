from ephem import *
import numpy as np
import pylab as plt
import glob, os
import inittasks as it
import plotutilities as plutil
import redpipe as pipe
import sys, getopt
import healpy as hp
import pyfits as pf

class stripe():

      def __init__(self):
          pass

      def call_mk_map_mod(self):

          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")

             mk_file = it.PATH_CODE + "mk_map_mod.py"

             file_names = glob.glob("*B.fits")
          
             for file_name in file_names:
	         command = "python "+mk_file+" "+file_name+" -i -m "+file_name[:-6]+"H.fits "+"-n --nside="+str(256)
                 print("CMD >>> "+command)
                 os.system(command)  
             os.chdir(it.PATH_CODE)

      

      def plot_healpix(self,file_name="zen.2457545.47315.xx.HH.uvcU_healpix.fits"):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             
             #file_names = glob.glob("*_healpix.fits") 

             haslam = hp.read_map(file_name,field=0)
            
             for x in xrange(len(haslam)):
                 if np.allclose(haslam[x],0.0):
                    haslam[x] = hp.UNSEEN 

             print "haslam = ",haslam

             proj_map = hp.mollview(haslam,coord=['C'], xsize=2000,return_projected_map=True,title=file_name,max=0.4)
             hp.graticule()
             plt.show()

             #mask = hp.read_map(file_name).astype(np.bool)
             #haslam_mask = hp.ma(mask)
             #haslam_mask.mask = np.logical_not(mask)
             #hp.mollview(haslam_mask.filled())
             #plt.show()
             os.chdir(it.PATH_CODE)

      def call_save_map(self):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")

             s_file = it.PATH_CODE + "save_map.py"

	     command = "python "+s_file+" *H.fits "+"-s all_sky.fits"
             print("CMD >>> "+command)
             os.system(command) 
	     os.chdir(it.PATH_CODE) 

      def create_gauss_beams_fits(self):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             
             file_names = glob.glob("*uvcU.fits")

             for file_name in file_names:
                 self.create_gauss_beam_fits(input_image=file_name)
             os.chdir(it.PATH_CODE)

      def create_gauss_beam_fits(self,input_image="zen.2457545.47315.xx.HH.uvcU.fits",produce_beam=True,produce_beam_sqr=True,apply_beam=True):
	  
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             fh = pf.open(input_image)
          
             image = fh[0].data

             #print "fh[0].header = ", fh[0].header

             cell_dim = np.absolute(fh[0].header["CDELT1"])
             n = fh[0].header["NAXIS1"]

             #TODO:: READ FREQ FROM HEADER OF FITS

	     #print "cell_dim = ",cell_dim
             #print "n = ",n

             #ASSUMING 14m DISH
             #ASSUMING OBS FREQ IS 150MHz
             #FWHM = 2.35*sigma

             lambda_v = 3e8/150e6

             p_beam = 1.22*lambda_v/14.0
         
             p_beam_deg = p_beam*(180.0/np.pi) 

             #print "b_beam_deg = ",p_beam_deg

             sigma = p_beam_deg/2.35

             #print "sigma = ",sigma
          
             fh.close()

             old_image = np.copy(image[0,0,:,:])
             image_v = image[0,0,:,:]
             
             x_0 = -1*(n/2.0)*cell_dim
             y = (n/2.0)*cell_dim

             for i in xrange(n):
                 x = x_0
                 
                 for j in xrange(n):
                     image_v[i,j] = np.exp(-1*(x**2/(2*sigma**2) + y**2/(2*sigma**2)))  
                     x += cell_dim
                     #print "x = ",x
                     #print "y = ",y
                 
                 y -= cell_dim
                 #print "y = ",y
                 #return x                          
             #plt.imshow(image_v)

             #plt.show()
             fh.close()
            
             if produce_beam:
                output_image = input_image[:-9]+"B.fits"
                cmd = 'cp ' + input_image + ' ' + output_image 
                print("CMD >>> "+cmd)
                os.system(cmd)           
                fh = pf.open(output_image)
                fh[0].data[0,0,:,:] = image_v
                #plt.imshow(image_v)
                #plt.show()
                fh.writeto(output_image,clobber=True)
                fh.close()	

             if produce_beam_sqr:
                output_image = input_image[:-9]+"sB.fits"
                cmd = 'cp ' + input_image + ' ' + output_image 
                print("CMD >>> "+cmd)
                os.system(cmd)           
                fh = pf.open(output_image)
                fh[0].data[0,0,:,:] = image_v**2
                fh.writeto(output_image,clobber=True)
                #plt.imshow(image_v**2)
                #plt.show()
                fh.close()	

             if apply_beam:
                output_image = input_image[:-6]+"B.fits"
                cmd = 'cp ' + input_image + ' ' + output_image 
                print("CMD >>> "+cmd)
                os.system(cmd)           
                fh = pf.open(output_image)
                fh[0].data[0,0,:,:] = image_v*old_image
                fh.writeto(output_image,clobber=True)
                #plt.imshow(image_v*old_image)
                #plt.show()
                fh.close()	
             
             os.chdir(it.PATH_CODE) 
           
             
if __name__ == "__main__":
   s = stripe()
   #s.call_mk_map_mod()
   #s.plot_healpix()
   s.create_gauss_beams_fits()
   s.call_mk_map_mod()
   #s.plot_healpix(file_name="zen.2457545.47315.xx.HH.uvcU.fits")
   #s.call_save_map()  
