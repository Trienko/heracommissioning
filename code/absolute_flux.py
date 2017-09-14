from ephem import *
import numpy as np
import pylab as plt
import glob, os
import inittasks as it
import plotutilities as plutil
import sys, getopt
import pyfits
import pickle

#FAINTER SOURCE (MEASURED WITH VIEWER)
PMN_J2101_2802_RA = "21:01:18.3"
PMN_J2101_2802_DEC = "-28:01:55"
PMN_J2101_2802_FLUX_189 = 23.1
PMN_J2101_2802_FLUX_150 = 23.1*(150.0/189.0)**(-0.8)

#https://ned.ipac.caltech.edu/cgi-bin/objsearch?objname=PMN+J2101-2802&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES


#BRIGHTER SOURCE (MEASURED WITH VIEWER)
PMN_J2107_2526_RA = "21:07:25.3"
PMN_J2107_2526_DEC = "-25:25:40"
PMN_J2107_2526_FLUX_189 = 47.7
PMN_J2107_2526_FLUX_150 = 47.7*(150.0/189.0)**(-0.8)

#https://ned.ipac.caltech.edu/cgi-bin/objsearch?objname=PMN+J2107-2526&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES


#OTHER OBSERVABLE SOURCE IDENTIFIED AS CENA
CENA_RA = "13:35:58"
CENA_DEC = "-34:04:19"

ABS_CAL_P = ''

class absflux():

      def __init__(self):
          pass

      def getFieldCenter(self,direc,fits_file):
          #print "d+f = ",direc+fits_file
          if os.path.isfile(direc+fits_file):
             ff = pyfits.open(direc+fits_file)
             header_v = ff[0].header
             ra_0 = header_v["crval1"]#degrees
             dec_0 = header_v["crval2"]#degrees
             ff.close()
          else:
             ra_0 = np.NaN
             dec_0 = np.NaN
          return ra_0,dec_0

      # converting ra and dec to l and m coordiantes
      def radec2lm(self,direc,fits_file,ra_d,dec_d):
          # ra and dec in degrees
          rad2deg = lambda val: val * 180./np.pi
          deg2rad = lambda val: val * np.pi/180
          ra0,dec0 = self.getFieldCenter(direc,fits_file) # phase centre in degrees
          #print "ra0 = ",ra0
          #print "dec0 = ",dec0
          ra0,dec0 = deg2rad(ra0),deg2rad(dec0)
          ra_r, dec_r = deg2rad(ra_d), deg2rad(dec_d) # coordinates of the sources in radians
          l = np.cos(dec_r)* np.sin(ra_r - ra0)
          m = np.sin(dec_r)*np.cos(dec0) - np.cos(dec_r)*np.sin(dec0)*np.cos(ra_r-ra0)
          return rad2deg(l),rad2deg(m) #lm in degrees

      def convert_PMN_J2101_2802_to_lm(self,direc,fits_file):
          ra_d = (hours(PMN_J2101_2802_RA))*180./np.pi
          dec_d = (degrees(PMN_J2101_2802_DEC))*180./np.pi

          l,m = self.radec2lm(direc,fits_file,ra_d,dec_d)
          return l,m

      def convert_PMN_J2107_2526_to_lm(self,direc,fits_file):
          ra_d = (hours(PMN_J2107_2526_RA))*180./np.pi
          dec_d = (degrees(PMN_J2107_2526_DEC))*180./np.pi

          l,m = self.radec2lm(direc,fits_file,ra_d,dec_d)
          return l,m

      def test_lm_conversion(self,direc,fits_file,l,m):
          if os.path.isfile(direc+fits_file):
             ff = pyfits.open(direc+fits_file)
             header_v = ff[0].header
             cellsize = np.absolute(header_v['cdelt1']) #pixel width in degrees
             #print "cellsize = ",cellsize
             #print "cellsize2 = ",header_v['cdelt2']
             #print "cellsize3 = ",header_v['cdelt1']
             data = ff[0].data
             data = data[0,0,::-1,::-1]
             npix = data.shape[0] #number of pixels in fits file
             cpix = npix/2.0
             max_l = int(cpix*cellsize)
             plt.imshow(data,extent=[-max_l,max_l,-max_l,max_l])
             plt.hold('on')
             plt.plot(l,m,'x',ms = 10.0)
             plt.show()
          else:
             pass

      def flipTrimBox(self,box,npix):
          x = np.arange(npix,dtype=int)
          x_reverse = x[::-1]
          #print "x_reverse = ",x_reverse
          #print "box = ",box
          itemindex1 = np.where(x_reverse==box[0])[0][0]
          itemindex2 = np.where(x_reverse==box[1])[0][0]
          itemindex3 = np.where(x_reverse==box[2])[0][0]
          itemindex4 = np.where(x_reverse==box[3])[0][0]

          #print "itemindex1 = ",itemindex1
          #print "itemindex2 = ",itemindex2
          #print "itemindex3 = ",itemindex3
          #print "itemindex4 = ",itemindex4
          return np.array([itemindex2,itemindex1,itemindex4,itemindex3])

      def obtainTrimBox(self,direc,fits_file,mask,window=2,pix_deg="PIX",plot_selection=False,avg=False):
          if not (os.path.isfile(direc+fits_file)):
             return np.array([np.NaN,np.NaN,np.NaN,np.NaN]),np.NaN,-1
          
          flux = np.zeros((mask.shape[0],),dtype=float)

          ff = pyfits.open(direc+"/"+fits_file)
          header_v = ff[0].header
          cellsize = np.absolute(header_v['cdelt1']) #pixel width in degrees
          data = ff[0].data
          data = data[0,0,::-1,::-1]
          npix = data.shape[0] #number of pixels in fits file

          cpix = npix/2.0

          values = np.zeros((mask.shape[0],3))

          if pix_deg == "PIX":
             w = window
          else:
             w = int(window/cellsize)+1

          for s in xrange(mask.shape[0]):
              l = mask[s,0]
              m = mask[s,1]
              source = True
              pix_x = int(cpix + l/cellsize)
              pix_y = int(cpix - m/cellsize)

              if pix_x < 0 or pix_x > npix:
                 source = False
              if pix_y < 0 or pix_y > npix:
                 source = False

              if source:
                 if pix_x - w < 0:
                    x_1 = 0
                 else:
                    x_1 = pix_x - w
                 if pix_x + w + 1> npix-1:
                    x_2 = npix-1
                 else:
                    x_2 = pix_x + w + 1
                 if pix_y - w < 0:
                    y_1 = 0
                 else:
                    y_1 = pix_y - w
                 if pix_y + w + 1 > npix-1:
                    y_2 = npix-1
                 else:
                    y_2 = pix_y + w + 1

                #print "y_1 = ",y_1
                #print "y_2 = ",y_2
              data_temp = np.copy(data[y_1:y_2,x_1:x_2])
              if avg:
                 flux[s] = np.average(data_temp)
              else:
                 flux[s] = np.amax(data_temp)	
	
              if plot_selection:
                   
                   #data[y_1:y_2,x_1:x_2] = 0
                   #data_temp = data[0:1000,:]

                   plt.imshow(data_temp)
                   plt.show()
                   plt.imshow(data)
                   plt.show()
              #else:
              #   x_1 = np.NaN
              #   x_2 = np.NaN
              #   y_1 = np.NaN
              #   y_2 = np.NaN
          ff.close()
          return flux

      def obtain_MS_range(self,source="PMN J2101-2802",before_after=3,print_values=False):
          
          if source == "PMN J2101-2802":
             S = hours(PMN_J2101_2802_RA)
          elif source == "PMN J2107 2526":
             S = hours(PMN_J2107_2526_RA)
          else:
             S = hours(PMN_J2101_2802_RA)

          os.chdir(it.PATH_DATA)
          HERA = Observer()
          HERA.lat, HERA.long, HERA.elevation = '-30:43:17', '21:25:40.08', 0.0
          j0 = julian_date(0)

          file_names = glob.glob("*uvcU.ms")
          ra_cen = np.zeros((len(file_names),))
          k = 0        
 
          for file_name in file_names:
              file_name_split = file_name.split('.')
              lst = file_name_split[1]+'.'+file_name_split[2]
              HERA.date = float(lst) - j0
              ra_cen[k] = float(HERA.sidereal_time())
              k = k + 1
              if print_values:
                 print "MSNAME: %s, UTC: %s (LST %s = %f)" % (file_name, HERA.date, HERA.sidereal_time(), float(HERA.sidereal_time()) )
	    
          d = np.absolute(ra_cen - S)
          index_min = np.argsort(d)
          
             
          ra_sorted = ra_cen[index_min]
          #print "ra_sorted = ",ra_sorted
    
          file_names_np = np.array(file_names)

          names_sorted = file_names_np[index_min]
          #print "names_sorted = ",names_sorted    
      
          os.chdir(it.PATH_CODE)
          return ra_sorted[:2*before_after], names_sorted[:2*before_after]
      
      def apply_c(self):
          global ABS_CAL_P
                
          os.chdir(it.PATH_DATA)
          if ABS_CAL_P == '':
             file_names = glob.glob("*ABS_CAL.p")
             ABS_CAL_P = file_names[0]
          file_names = glob.glob("*uvcU.ms")
          for file_name in file_names:
              command = "cp -r "+file_name+" "+file_name[:-3]+"C.ms"
              print("CMD >>> "+command)
              os.system(command)
              file = open("abs_flux_cal.py","w")
              file.write("from casa import table as tb\n") 
              file.write("tb.open(\""+file_name[:-3]+"C.ms"+"\",nomodify=False)\n")
              file.write("corrected_data = tb.getcol(\"CORRECTED_DATA\")\n")
              file.write("import pickle\n")
              file.write("input = open(\""+ABS_CAL_P+"\",\'rb\')\n")
              file.write("c = pickle.load(input)\n")
              file.write("input.close()\n")
              file.write("corrected_data = c*corrected_data\n")
              file.write("tb.putcol(\"CORRECTED_DATA\",corrected_data)\n")
              file.write("tb.flush()\n")
              file.write("tb.close()\n")
              file.close()
              command = "casa -c abs_flux_cal.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
              #break
          os.chdir(it.PATH_CODE)

      def apply_c_spec(self):
          global ABS_CAL_P

          temp_dir = it.PATH_DATA
          it.PATH_DATA = it.SPEC_GC_DIR 
                
          os.chdir(it.PATH_DATA)
          if ABS_CAL_P == '':
             file_names = glob.glob("*ABS_CAL.p")
             ABS_CAL_P = file_names[0]
             
             command = "cp -r "+it.SPEC_GC_DIR+ABS_CAL_P+" "+temp_dir+"."
             print("CMD >>> "+command)
             os.system(command)

          it.PATH_DATA = temp_dir
          os.chdir(it.PATH_DATA)

          file_names = glob.glob("*uvcU.ms")
          for file_name in file_names:
              command = "cp -r "+file_name+" "+file_name[:-3]+"C.ms"
              print("CMD >>> "+command)
              os.system(command)
              file = open("abs_flux_cal.py","w")
              file.write("from casa import table as tb\n") 
              file.write("tb.open(\""+file_name[:-3]+"C.ms"+"\",nomodify=False)\n")
              file.write("corrected_data = tb.getcol(\"CORRECTED_DATA\")\n")
              file.write("import pickle\n")
              file.write("input = open(\""+ABS_CAL_P+"\",\'rb\')\n")
              file.write("c = pickle.load(input)\n")
              file.write("input.close()\n")
              file.write("corrected_data = c*corrected_data\n")
              file.write("tb.putcol(\"CORRECTED_DATA\",corrected_data)\n")
              file.write("tb.flush()\n")
              file.write("tb.close()\n")
              file.close()
              command = "casa -c abs_flux_cal.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
              #break
          os.chdir(it.PATH_CODE)

      def compute_c(self):
          global ABS_CAL_P
          mask = np.zeros((2,2),dtype=float)
          direc = plutil.FIGURE_PATH+"IMAGES/"
          direc_data = it.PATH_DATA
          direc_img = plutil.FIGURE_PATH+"CAL_SOLUTIONS/"

          ra,names = self.obtain_MS_range(source="PMN J2101-2802",before_after=2)
          ind = np.argsort(ra)
          ra = ra[ind]
          names = names[ind]

          splt = names[0].split('.')
          pickle_name = splt[1]+'_ABS_CAL.p'
          ABS_CAL_P = pickle_name 
          JD = splt[1] 

          source_flux = np.zeros((2,len(names)),dtype=float)
          beam_gain = np.zeros((2,len(names)),dtype=float)
          x = 0
   
          for fits_file in names:
              fits_file = fits_file[:-2]+"fits"
              beam_fits = fits_file[:-9]+"B.fits"

              print

              l,m = self.convert_PMN_J2101_2802_to_lm(direc,fits_file)

              mask[0,0] = l
              mask[0,1] = m

              l,m = self.convert_PMN_J2107_2526_to_lm(direc,fits_file)

              mask[1,0] = l
              mask[1,1] = m

              source_flux[:,x] = self.obtainTrimBox(direc,fits_file,mask,window=8,pix_deg="PIX",plot_selection=False) 
              beam_gain[:,x] = self.obtainTrimBox(direc,beam_fits,mask,window=3,pix_deg="PIX",plot_selection=False,avg=True) 
              x = x + 1

          fact1 = np.sum(beam_gain[0,:]*source_flux[0,:])/np.sum(beam_gain[0,:]**2)
          fact2 = np.sum(beam_gain[1,:]*source_flux[1,:])/np.sum(beam_gain[1,:]**2)

          c1 = PMN_J2101_2802_FLUX_150/fact1
          c2 = PMN_J2107_2526_FLUX_150/fact2
          c3 = (PMN_J2101_2802_FLUX_150+PMN_J2107_2526_FLUX_150)/(fact1 + fact2)
        
          if os.path.isfile(direc_data+pickle_name):  
             command = "rm "+direc_data+pickle_name
             print "CMD >> ",command
             os.system(command)         
         
          output = open(direc_data+pickle_name, 'wb')
          pickle.dump(c3, output)
          output.close()

          if not os.path.isdir(direc_img):
             command = "mkdir "+direc_img
             print "CMD >> ",command
             os.system(command) 

          plt.plot(ra,source_flux[0,:],label="PMN J2101-2802")
          plt.plot(ra,source_flux[1,:],label="PMN J2107-2526")
          plt.legend()
          plt.xlabel("RA [rad]")
          plt.ylabel("Uncalibrated Flux")
          plt.savefig(direc_img+JD+"_UN_CAL.png")
          plt.clf()

          plt.plot(ra,beam_gain[0,:],label="PMN J2101-2802")
          plt.plot(ra,beam_gain[1,:],label="PMN J2107-2526")
          plt.legend()
          plt.xlabel("RA [rad]")
          plt.ylabel("Beam Gain")
          plt.savefig(direc_img+JD+"_BEAM.png")
          plt.clf()

          plt.plot(ra,source_flux[0,:]*c3,label="PMN J2101-2802")
          plt.plot(ra,source_flux[1,:]*c3,label="PMN J2107-2526")
          plt.legend()
          plt.xlabel("RA [rad]")
          plt.savefig(direc_img+JD+"_CAL.png")
          plt.clf()
          #plt.show()

          return c3

def main(argv):
    a = absflux()
    abscal = False
    applycal = False
    apply_spec = False

    try:
       opts, args = getopt.getopt(argv,"h", ["abs_cal","apply_spec","set_data_path="])
    except getopt.GetoptError:
       print 'python absolute_flux.py --abs_cal --apply_spec --set_data_path <path>'
       sys.exit(2)
    for opt, arg in opts:
        print "opt = ",opt
        print "arg = ",arg
        if opt == '-h':
           print 'python absolute_flux.py --abs_cal --apply_spec'
           print '--abs_cal: 1. Absolute calibrate the data using PMN J2101 2802 and PMN J2107 2526. 2. Apply to all ms in JD dir.'
           print '--apply_spec: Apply the absolute scaling from the JD pointed to by SPEC_GC_DIR"
           print '--set_data_path: sets the path to the data directory'
           sys.exit()
        elif opt == "--set_data_path":
             it.PATH_DATA = arg
        elif opt == "--abs_cal":
             #print "HALLO"
             abscal = True
             applycal = True
        elif opt == "--apply_spec":
             apply_spec = True
    if abscal:
        c = a.compute_c()
        print "c = ",c
    if applycal:
        a.apply_c()
    if apply_spec:
        a.apply_c_spec()
             

if __name__ == "__main__":
   main(sys.argv[1:])
   #ab_object = absflux()
   #c = ab_object.compute_c()
   #print "c = ",c 
   #ab_object.apply_c()  


   '''
   ab_object = absflux()
   
   mask = np.zeros((2,2),dtype=float)
   direc = plutil.FIGURE_PATH+"IMAGES/"
   
   ra,names = ab_object.obtain_MS_range(source="PMN J2101-2802",before_after=2)
   ind = np.argsort(ra)
   ra = ra[ind]
   names = names[ind]

   source_flux = np.zeros((2,len(names)),dtype=float)
   beam_gain = np.ze1ros((2,len(names)),dtype=float)
   x = 0
   
   for fits_file in names:
       fits_file = fits_file[:-2]+"fits"
       beam_fits = fits_file[:-9]+"B.fits"

       print "fits_file = ",fits_file
       print "beam_fits = ",beam_fits

       print "direc = ",direc
       l,m = ab_object.convert_PMN_J2101_2802_to_lm(direc,fits_file)

       print "l = ",l
       print "m = ",m

       mask[0,0] = l
       mask[0,1] = m

       l,m = ab_object.convert_PMN_J2107_2526_to_lm(direc,fits_file)

       mask[1,0] = l
       mask[1,1] = m

       source_flux[:,x] = ab_object.obtainTrimBox(direc,fits_file,mask,window=8,pix_deg="PIX",plot_selection=True) 
       beam_gain[:,x] = ab_object.obtainTrimBox(direc,beam_fits,mask,window=2,pix_deg="PIX",plot_selection=True,avg=True) 
       x = x + 1
       #print "flux = ",flux

   plt.plot(ra,source_flux[0,:],label="PMN J2101-2802")
   plt.plot(ra,source_flux[1,:],label="PMN J2107-2526")
   plt.legend()
   plt.xlabel("RA [rad]")
   plt.ylabel("Uncalibrated Flux")
   plt.show()

   plt.plot(ra,beam_gain[0,:],label="PMN J2101-2802")
   plt.plot(ra,beam_gain[1,:],label="PMN J2107-2526")
   plt.legend()
   plt.xlabel("RA [rad]")
   plt.ylabel("Beam Gain")
   plt.show()

   plt.plot(ra,beam_gain[0,:]**(2),label="PMN J2101-2802")
   plt.plot(ra,beam_gain[1,:]**(2),label="PMN J2107-2526")
   plt.legend()
   plt.xlabel("RA [rad]")
   plt.ylabel("Beam Gain")
   plt.show()

   plt.plot(ra,source_flux[0,:]/beam_gain[0,:],label="PMN J2101-2802")
   plt.plot(ra,source_flux[1,:]/beam_gain[1,:],label="PMN J2107-2526")
   plt.legend()
   plt.xlabel("RA [rad]")
   plt.ylabel("Uncalibrated Flux")
   plt.show()

   fact1 = np.sum(beam_gain[0,:]*source_flux[0,:])/np.sum(beam_gain[0,:]**2)
   fact2 = np.sum(beam_gain[1,:]*source_flux[1,:])/np.sum(beam_gain[1,:]**2)

   c1 = PMN_J2101_2802_FLUX_150/fact1
   c2 = PMN_J2107_2526_FLUX_150/fact2
   c3 = (PMN_J2101_2802_FLUX_150+PMN_J2107_2526_FLUX_150)/(fact1 + fact2) 

   print "c1 = ",c1
   print "c2 = ",c2
   print "c3 = ",c3
   print "PMN_J2101_2802_FLUX_150 = ",PMN_J2101_2802_FLUX_150
   print "PMN_J2107_2526_FLUX_150 = ",PMN_J2107_2526_FLUX_150

   plt.plot(ra,source_flux[0,:]*c3,label="PMN J2101-2802")
   plt.plot(ra,source_flux[1,:]*c3,label="PMN J2107-2526")
   plt.legend()
   plt.xlabel("RA [rad]")
   plt.ylabel("Calibrated Flux [Jy]")
   plt.show()

   plt.plot(ra,source_flux[0,:]/beam_gain[0,:]*c3,label="PMN J2101-2802")
   plt.plot(ra,source_flux[1,:]/beam_gain[1,:]*c3,label="PMN J2107-2526")
   plt.legend()
   plt.xlabel("RA [rad]")
   plt.ylabel("Calibrated Flux")
   plt.show()
   '''
   

 

