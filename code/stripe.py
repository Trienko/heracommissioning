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
	         command = "python "+mk_file+" "+file_name+" -i -m "+file_name[:-5]+"H.fits "+"-n --nside="+str(256)
                 print("CMD >>> "+command)
                 os.system(command)  
             os.chdir(it.PATH_CODE)

      
      #m=None
      #w=None
      #for fits in args:
      #    print 'Opening:',fits
      #    fitssplt = fits.split('/')[-1].split('.')
      #    JD = fitssplt[0] + '.' + fitssplt[1]
         #POL = 'xx'
         #beam = '%s.%s.B_healpix.fits'%(JD,POL)
      #    path,srcFits=os.path.split(os.path.realpath(fits))
         #destBm = os.path.join(path,beam)
      #    if m is None: 
      #        m,w,hdr=h.read_map(fits,field=(0,1),h=True)
             #bm,bw,bhdr=h.read_map(destBm,field=(0,1),h=True)
      #    else:
      #        m0,w0,hdr=h.read_map(fits,field=(0,1),h=True)
             #bm0,bw0,bhdr=h.read_map(destBm,field=(0,1),h=True)
      #        m+=m0
      #        w+=w0
             #bm+=bm0
      #if not(opts.savemap is None):
      #    ofn=opts.savemap
         #h.write_map(ofn,n.array([m/bm,w,w]),dtype=n.float64,coord='E')
      #    h.write_map(ofn,n.array([m,w,w]),dtype=n.float64,coord='E')

      def make_all_sky_map(self):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"): 
             os.chdir(plutil.FIGURE_PATH+"IMAGES/")     
             file_names = glob.glob("*uvcUBH.fits")
             m = None
             w = None

             for file_name in file_names:
                 beam_name = file_name[:-11]+"sBH.fits"
                 if m is None:
                    #print "file_name = ",file_name
                    m = hp.read_map(file_name,field=0)
                 else:
                    m = m + hp.read_map(file_name,field=0)  
                 if w is None:
                    #print "beam_name = ",beam_name
                    w = hp.read_map(beam_name,field=0)
                 else:
                    w = w + hp.read_map(beam_name,field=0)

             c = np.copy(m)

             for k in xrange(len(m)):
                 if not w[k]<0.01:
                    c[k] = m[k]/w[k]
                 else:
                    c[k] = 0       

             #with np.errstate(divide='ignore', invalid='ignore'):
             #     c = np.true_divide(m,w)
             #     c[c == np.inf] = 0
             #     #c = np.nan_to_num(c)
                   
             hp.write_map("ALL_SKY.fits",np.array([c,m,w]),dtype=np.float64,coord='C')            
 
      def plot_healpix(self,file_name="Abhik.fits",field=0):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             
             #file_names = glob.glob("*_healpix.fits") 

             haslam = hp.read_map(file_name,field=field)
            
             for x in xrange(len(haslam)):
                 if np.allclose(haslam[x],0.0):
                    haslam[x] = hp.UNSEEN 

             #print "haslam = ",haslam

             proj_map = hp.mollview(haslam,coord=['C'], xsize=2000,return_projected_map=True,title=file_name)#max=0.4
             hp.graticule()
             f = file_name[:-5]
             plt.savefig(plutil.FIGURE_PATH+"IMAGES/"+f+str(field)+".png")          

             #plt.show()

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
          #print plutil.FIGURE_PATH+"IMAGES/"
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             #print "halo"
             file_names = glob.glob("*uvcU.fits")
             #print "file_names = ",file_names
             for file_name in file_names:
                 #print "file_name ",file_name
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
                output_image = input_image[:-5]+"B.fits"
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

def main(argv):
    s = stripe()
    createbeams = False
    mkmod = False
    allsky = False
    plthlpx = False
   

    try:
       opts, args = getopt.getopt(argv,"h", ["create_beams","call_mk_map_mod","make_all_sky_map","plot_healpix"])
    except getopt.GetoptError:
       print 'python stripe.py --create_beams --call_mk_map_mod --make_all_sky_map --plot_healpix'
       sys.exit(2)
    for opt, arg in opts:
        #print "opt = ",opt
        #print "arg = ",arg
        if opt == '-h':
           print 'python stripe.py --create_beams --call_mk_map_mod --make_all_sky_map --plot_healpix'
           print '--create_beams: creating different kind of beam files, a beam, a beam times sky and a beam square file'
           print '--call_mk_map_mod: project all fits files to individual healpix projected fits files'
           print '--make_all_sky_map: make an all sky healpix map from the individual healpix-fits files (use squared beam weighting)'
           print '--plot_healpix: plot the all sky healpix'
           sys.exit()
        elif opt == "--create_beams":
           createbeams = True
        elif opt == "--call_mk_map_mod":
           mkmod = True
        elif opt == "--make_all_sky_map":
           allsky = True  
        elif opt == "--plot_healpix":
           plthlpx = True 

    if createbeams:
        s.create_gauss_beams_fits()
    if mkmod:
        s.call_mk_map_mod()
    if allsky:
        s.make_all_sky_map()
    if plthlpx:
	s.plot_healpix(file_name="ALL_SKY.fits",field=0)
        s.plot_healpix(file_name="ALL_SKY.fits",field=1)
        s.plot_healpix(file_name="ALL_SKY.fits",field=2)
           
             
if __name__ == "__main__":
   main(sys.argv[1:])
   #s = stripe()
   #s.call_mk_map_mod()
   #s.plot_healpix()
   #s.create_gauss_beams_fits()
   #s.call_mk_map_mod()
   #s.make_all_sky_map()
   #s.plot_healpix(file_name="ALL_SKY.fits")
   #s.plot_healpix(file_name="zen.2457545.47315.xx.HH.uvcU.fits")
   #s.call_save_map()  
