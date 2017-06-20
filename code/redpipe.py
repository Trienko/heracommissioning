from ephem import *
import numpy as np
import pylab as plt
import glob, os
import inittasks as it
import plotutilities as plutil
import sys, getopt
import pyfits as pf

#510~512
FLAG_SPW_STRING = '0:0~140;379~387;510~512;768~770;851~852;901~1023'
#FLAG_SPW_STRING = '0:0~140;901~1023'
FLAG_ANT_STRING = '81;82;113'
SGR_STR = '17:45:40.0'
SGR_FLOAT = (17.0 + 45.0/60 + 40.0/3600)*(pi/12)
BANDBASS_GC_CAL_TABLE = ''
DELAY_GC_CAL_TABLE = ''
POINT_SOURCE_MODEL = 'point_source_model.cl'
AO_STRATEGY = 'cool_strategy.rfis'

class redpipe():

      def __init__(self):
          pass

      #####################################
      #CASA wrapper around flagdata 
      #####################################
      def flagdata_wrapper(self,options={}):
          it.CASA_WRAPPER(task="flagdata",options=options)
          print os.getcwd()
          command = "casa -c flagdata_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around ft 
      #####################################
      def ft_wrapper(self,options={}):
          it.CASA_WRAPPER(task="ft",options=options)
          print os.getcwd()
          command = "casa -c ft_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around bandpass 
      #####################################
      def bandpass_wrapper(self,options={}):
          it.CASA_WRAPPER(task="bandpass",options=options)
          print os.getcwd()
          command = "casa -c bandpass_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around gaincal 
      #####################################
      def gaincal_wrapper(self,options={}):
          it.CASA_WRAPPER(task="gaincal",options=options)
          print os.getcwd()
          command = "casa -c gaincal_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around plotcal 
      #####################################
      def plotcal_wrapper(self,options={}):
          it.CASA_WRAPPER(task="plotcal",options=options)
          print os.getcwd()
          command = "casa -c plotcal_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around applycal 
      #####################################
      def applycal_wrapper(self,options={}):
          it.CASA_WRAPPER(task="applycal",options=options)
          print os.getcwd()
          command = "casa -c applycal_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around clean
      #####################################
      def clean_wrapper(self,options={}):
          it.CASA_WRAPPER(task="clean",options=options)
          print os.getcwd()
          command = "casa -c clean_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around viewer
      #####################################
      def viewer_wrapper(self,options={}):
          it.CASA_WRAPPER(task="viewer",options=options)
          print os.getcwd()
          command = "casa -c viewer_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around viewer
      #####################################
      def exportfits_wrapper(self,options={}):
          it.CASA_WRAPPER(task="exportfits",options=options)
          print os.getcwd()
          command = "casa -c exportfits_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around importfits
      #####################################
      def importfits_wrapper(self,options={}):
          it.CASA_WRAPPER(task="importfits",options=options)
          print os.getcwd()
          command = "casa -c importfits_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      def flag_basic_all(self):
          
          os.chdir(it.PATH_DATA)
          
          #FLAG BAD CHANNELS
          ##################
          options={}          
          options["mode"]='manual'
          options["action"]='apply'
          options["datacolumn"]='DATA'
          options["spw"] = FLAG_SPW_STRING  
          

          for file_name in glob.glob("*.ms"):
              options["vis"]=file_name
              self.flagdata_wrapper(options=options)

          #FLAG BAD ANT
          ##################
          options={}          
          options["mode"]='manual'
          options["action"]='apply'
          options["datacolumn"]='DATA'
          options["antenna"] = FLAG_ANT_STRING  

          for file_name in glob.glob("*.ms"):
              options["vis"]=file_name
              self.flagdata_wrapper(options=options)

          #FLAG AUTO
          ##################
          options={}          
          options["mode"]='manual'
          options["action"]='apply'
          options["datacolumn"]='DATA'
          options["autocorr"] = True  

          for file_name in glob.glob("*.ms"):
              options["vis"]=file_name
              self.flagdata_wrapper(options=options)
          
          os.chdir(it.PATH_CODE)

      def flag_aoflagger(self):
          
          for file_name in glob.glob(it.PATH_DATA+"*.ms"):
              command = "aoflagger -strategy "+AO_STRATEGY+" "+file_name
              print("CMD >>> "+command)
              os.system(command)
     
      def print_lst(self,print_values=False):
          print it.PATH_DATA
          os.chdir(it.PATH_DATA)
          HERA = Observer()
          HERA.lat, HERA.long, HERA.elevation = '-30:43:17', '21:25:40.08', 0.0
          j0 = julian_date(0)

          file_names = glob.glob("*.ms")
          print file_names
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
	    
          d = np.absolute(ra_cen - SGR_FLOAT)
          index_min = np.argmin(d)
          msname = file_names[index_min]
          if print_values:
             print "SGR = ",SGR_STR 
             #for k in xrange(len(ra_cen)):
             #    print file_names[k]+" "+str(ra_cen[k])+" "+str(SGR_FLOAT)+" "+str(d[k]) 
          #print msname
          os.chdir(it.PATH_CODE)
          return msname

      def bandpass_gc(self,delay=False):
          global BANDBASS_GC_CAL_TABLE
          global DELAY_GC_TABLE
          
          gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
          os.chdir(it.PATH_DATA)
          
          #CREATE POINT SOURCE MODEL AT THE POS OF GALACTIC CENTER
          if not os.path.isdir(POINT_SOURCE_MODEL):
             command = "casa -c create_ps.py --nogui --nologfile --log2term"
             print("CMD >>> "+command)
             os.system(command) 
             command = "rm ipython*.log"
             print("CMD >>> "+command)
             os.system(command)
          
          #FT POINT SOURCE MODEL
          options={}          
          options["vis"]=gc_name
          options["complist"]=POINT_SOURCE_MODEL
          options["usescratch"]=True
          self.ft_wrapper(options=options)

          gc_name_split = gc_name.split('.')
          gc_jd = gc_name_split[1]+'.'+gc_name_split[2]
          
          if delay:
             DELAY_GC_CAL_TABLE = 'd_'+gc_jd+'.cal'
             options={}
             options["vis"]=gc_name
             options["solint"]='inf'
             options["combine"]='scan'
             options["refant"]='10'
             options["spw"]="0:0~1023"
             options["gaintype"]='K'
             options["caltable"]=DELAY_GC_CAL_TABLE
             self.gaincal_wrapper(options=options)
             
          BANDBASS_GC_CAL_TABLE = 'b_'+gc_jd+'.cal'
          
          #BANDPASS CALIBRTION OF GC-MS WITH PS AT GALACTIC CENTER
          options={}
          options["vis"]=gc_name
          options["solint"]='inf'
          options["combine"]='scan'
          options["caltable"] = BANDBASS_GC_CAL_TABLE 
          if delay:
             options["gaintable"] = DELAY_GC_CAL_TABLE
          self.bandpass_wrapper(options=options)
          os.chdir(it.PATH_CODE)

      def plot_cal_gc(self,delay=False):
          global BANDBASS_GC_CAL_TABLE
          global DELAY_GC_CAL_TABLE 

          if BANDBASS_GC_CAL_TABLE == '':
             gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
	     gc_name_split = gc_name.split('.')
             gc_jd = gc_name_split[1]+'.'+gc_name_split[2]
          
             BANDBASS_GC_CAL_TABLE = 'b_'+gc_jd+'.cal'

          if DELAY_GC_CAL_TABLE == '':
             gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
	     gc_name_split = gc_name.split('.')
             gc_jd = gc_name_split[1]+'.'+gc_name_split[2]
          
             DELAY_GC_CAL_TABLE = 'd_'+gc_jd+'.cal'
           
          os.chdir(it.PATH_DATA)
                       
          if os.path.isdir(BANDBASS_GC_CAL_TABLE):
             if not os.path.isdir(plutil.FIGURE_PATH):
                command = "mkdir "+plutil.FIGURE_PATH
               	print("CMD >>> "+command)
             	os.system(command)

             if not os.path.isdir(plutil.FIGURE_PATH+"CAL_SOLUTIONS/"):
             	command = "mkdir "+plutil.FIGURE_PATH+"CAL_SOLUTIONS/"
             	print("CMD >>> "+command)
             	os.system(command)

             options={}
             options["caltable"]=BANDBASS_GC_CAL_TABLE
             options["xaxis"]='chan'
             options["yaxis"]='phase'
             options["showgui"]=False
             options["figfile"]=plutil.FIGURE_PATH+"CAL_SOLUTIONS/"+BANDBASS_GC_CAL_TABLE+"_PHASE.png"
	     self.plotcal_wrapper(options=options)

             options={}
             options["caltable"]=BANDBASS_GC_CAL_TABLE
             options["xaxis"]='chan'
             options["yaxis"]='amp'
             options["showgui"]=False
             options["figfile"]=plutil.FIGURE_PATH+"CAL_SOLUTIONS/"+BANDBASS_GC_CAL_TABLE+"_AMP.png"
	     self.plotcal_wrapper(options=options)

          if delay:
             if os.path.isdir(DELAY_GC_CAL_TABLE):
                if not os.path.isdir(plutil.FIGURE_PATH):
                   command = "mkdir "+plutil.FIGURE_PATH
               	   print("CMD >>> "+command)
             	   os.system(command)

                if not os.path.isdir(plutil.FIGURE_PATH+"CAL_SOLUTIONS/"):
             	   command = "mkdir "+plutil.FIGURE_PATH+"CAL_SOLUTIONS/"
             	   print("CMD >>> "+command)
             	   os.system(command)

                #plotcal(caltable=delay_table,xaxis='antenna',yaxis='delay')
                options={}
                options["caltable"]=DELAY_GC_CAL_TABLE
                options["xaxis"]='antenna'
                options["yaxis"]='delay'
                options["showgui"]=False
                options["figfile"]=plutil.FIGURE_PATH+"CAL_SOLUTIONS/"+DELAY_GC_CAL_TABLE+"_DELAY.png"
	        self.plotcal_wrapper(options=options)
                
          os.chdir(it.PATH_CODE)

      def applycal_gc_all(self,delay=False):
          global BANDBASS_GC_CAL_TABLE
          global DELAY_GC_CAL_TABLE
          if BANDBASS_GC_CAL_TABLE == '':
             gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
	     gc_name_split = gc_name.split('.')
             gc_jd = gc_name_split[1]+'.'+gc_name_split[2]
          
             BANDBASS_GC_CAL_TABLE = 'b_'+gc_jd+'.cal'

          if DELAY_GC_CAL_TABLE == '':
             gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
	     gc_name_split = gc_name.split('.')
             gc_jd = gc_name_split[1]+'.'+gc_name_split[2]
          
             DELAY_GC_CAL_TABLE = 'd_'+gc_jd+'.cal'

          os.chdir(it.PATH_DATA)
          file_names = glob.glob("*.ms")
          for file_name in file_names:
              options={}
              options["vis"] = file_name
              if delay:
                 options["gaintable"]=[DELAY_GC_CAL_TABLE,BANDBASS_GC_CAL_TABLE]
              else:   
                 options["gaintable"]=BANDBASS_GC_CAL_TABLE
              
	      self.applycal_wrapper(options=options)
          os.chdir(it.PATH_CODE)

      def create_images(self,mask="U",n_block = 75, imp_factor = 30):
          os.chdir(it.PATH_DATA)
          
          if not os.path.isdir(plutil.FIGURE_PATH):
             command = "mkdir "+plutil.FIGURE_PATH
             print("CMD >>> "+command)
             os.system(command) 
             
          if not os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             command = "mkdir "+plutil.FIGURE_PATH+"IMAGES/"
             print("CMD >>> "+command)
             os.system(command)

          if mask == "U":
             file_names = glob.glob("*.ms")
          else:
             file_names = glob.glob("*C.ms")

          #print "file_names = ",file_names

          #file_names = ["zen.2457545.47315.xx.HH.uvcUC.ms"]

          for file_name in file_names:
              
              if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".model"):
                 command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".model"
                 print("CMD >>> "+command)
                 os.system(command)
                 command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".psf"
                 print("CMD >>> "+command)
                 os.system(command)
                 command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".residual"
                 print("CMD >>> "+command)
                 os.system(command)
                 command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".image"
                 print("CMD >>> "+command)
                 os.system(command)
                 #command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".fits"
                 #print("CMD >>> "+command)
                 #os.system(command)
                 command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".mask"
                 print("CMD >>> "+command)
                 os.system(command)
                 command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".png"
                 print("CMD >>> "+command)
                 os.system(command)
             
              #RUN THE CLEAN TASK
              options={}
              options["vis"] = file_name
              options["imagename"] = plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]
              options["imagermode"] = 'csclean'
              options["psfmode"] = 'clark'
              options["threshold"]='0.2Jy'
              options["niter"]=0
              options["mode"]='mfs'
              options["cell"]=['10arcmin','10arcmin']
              options["weighting"]='uniform'
              options["imsize"]=[240,240]
              options["gridmode"]='widefield'
              options["wprojplanes"]=128
              options["gain"]=0.2
              options["interactive"]=False

              #print plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".mask.txt"

              if mask == "C":
                 #print "HALLO C"
                 print plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".mask.txt"
                 print os.path.isfile(plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".mask.txt")
                 if os.path.isfile(plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".mask.txt"):
                    #print "HALLO 1"
                    if os.path.isfile(plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".fits"):
                       #print "HALLO 2"
                       file_name2 = plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".fits"
                       fh = pf.open(file_name2)
                       image = fh[0].data
                       image = np.copy(image[0,0,:,:])
                       #img_std = np.std(image[0:n_block,0:n_block])
                       max_v = np.amax(image[0:n_block,0:n_block])
		       options["threshold"]=str(max_v/imp_factor)+'Jy'
                       options["niter"]=100
                       mask_list = []
                       txt_file = open(file_name2[:-5]+".mask.txt","r") 
                       lines = txt_file.readlines()
                       txt_file.close()
                       options["mask"]=lines
                       fh.close()
            

	      self.clean_wrapper(options=options)

              #RUN VIEWER
              options={}
              options["infile"] = plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".image"
              options["outfile"] = plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".png"
              options["outformat"] = 'png'
              options["gui"]=False
            
              self.viewer_wrapper(options=options)
          os.chdir(it.PATH_CODE)

      def convert_to_fits(self,mask="U"):
	  if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):

             os.chdir(plutil.FIGURE_PATH+"IMAGES/")

             if mask == "U":
                file_names = glob.glob("*.image")
             else:
                file_names = glob.glob("*C.image")
          
             #print "file_names = ",file_names 
             #file_names = ["zen.2457545.47315.xx.HH.uvcUC.image"]

             for file_name in file_names:
                 #print file_name
                 options={}
                 options["imagename"] = file_name
                 options["fitsimage"] = file_name[:-6]+".fits"
                 options["history"]=False
                 options["overwrite"]= True
                 self.exportfits_wrapper(options)

          os.chdir(it.PATH_CODE)

      def produce_decon_mask(self,n_block = 75, thr_dr = 8.5, w_pixels=17):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             
             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             
             file_names = glob.glob("*uvcUC.fits")

             #file_names = ["zen.2457545.47315.xx.HH.uvcUC.fits"]

	     for file_name in file_names:
                 
                 mask_region = []                 
 
                 fh = pf.open(file_name)
                 image = fh[0].data
                 
                 image = np.copy(image[0,0,:,:])
                 old_image = np.copy(image)
                 N = old_image.shape[0]

                 mask_one = np.ones(image.shape)
                 counter = 0              

                 while True:

                       #print "counter = ",counter
  
                       if counter >= 4:
                          break

                       img_std = np.std(old_image[0:n_block,0:n_block])
                       img_peak = image.max()
                       
                       #print "file_name = ",file_name
                       #print "thr_dr*img = ",thr_dr*img_std
                       #print "img_peak = ",img_peak

                       if img_peak > thr_dr*img_std:
                          #print "file_name = ",file_name
                           
                          i = np.arange(image.shape[0])
                          j = np.arange(image.shape[0])

                          jj,ii = np.meshgrid(i,j)

                          #print "ii = ",ii
                          #print "jj = ",jj
                          #break

                          #plt.imshow(image)
                          #plt.show()
                          
                          idx_unr = np.unravel_index(image.argmax(), image.shape)

                          x = idx_unr[0]
                          y = idx_unr[1]

                          row = idx_unr[0]
                          column = idx_unr[1]

                          #print "x = ",x
                          #print "y = ",y

                          #print "row = ",row
                          #print "y_c = ",column

                          y_c = row
                          x_c = column

                          #print "x_c = ",x_c
                          #print "y_c = ",y_c

                          region = "circle [ [ "+str(int(x_c))+"pix , "+str(int(y_c))+"pix ] , "+str(int(w_pixels))+"pix ]" 
                          mask_region.append(region)

                          d_temp = np.sqrt((ii-x)**2 + (jj-y)**2)

                          mask_one[d_temp < w_pixels] = 0
                          #mask_zero[d_temp < w_pixels] = 1
                          image = mask_one*old_image
                          #plt.imshow(image)
                          #plt.show()
                          counter = counter + 1
                       else:
                          break 
                 fh.close()
                 
                 if len(mask_region) > 0:
                    output_file = file_name[:-5]+".mask.txt"
                    file = open(output_file,"w") 
                    for i in xrange(len(mask_region)):
                        file.write(mask_region[i])
                    file.close()
             os.chdir(it.PATH_CODE)
                 

             """ MAKING A FITS MASK (REPLACED BY CASA REGIONS)
             if make_mask:
                  
                    plt.imshow(old_image)
                    plt.title(file_name)
                    plt.show()

                    plt.imshow(mask_one*old_image)
                    plt.title(file_name)
                    plt.show()

                    output_image = file_name[:-5]+".mask.fits" 
                    cmd = 'cp ' + file_name + ' ' + output_image 
                    print("CMD >>> "+cmd)
                    os.system(cmd)           
                    fh = pf.open(output_image)
                    fh[0].data[0,0,:,:] = mask_zero
                    #plt.imshow(image_v)
                    #plt.show()
                    fh.writeto(output_image,clobber=True)
                    fh.close()	
                    options={}
                    options["imagename"] = output_image[:-5]
                    options["fitsimage"] = output_image
                    options["overwrite"]= True
                    self.importfits_wrapper(options)
             """
   

      def plot_peak_sigma(self):
          if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             
             os.chdir(plutil.FIGURE_PATH+"IMAGES/")
             
             file_names = glob.glob("*uvcU.fits") 

             x = np.zeros((len(file_names),))
             y_std = np.zeros((len(file_names),))
             y_peak = np.zeros((len(file_names),))
             y_10 = np.ones((len(file_names),))*9            

             counter = 0
             for file_name in file_names:
                 print "file_name = ",file_name
		 
                 splt = file_name.split('.')
                 x[counter] = int(splt[2])

                 fh = pf.open(file_name)
                          
                 image = fh[0].data

                 #print "fh[0].header = ", fh[0].header
                 #cell_dim = np.absolute(fh[0].header["CDELT1"])
                 #n = fh[0].header["NAXIS1"]
                 
                 old_image = np.copy(image[0,0,:,:])

                 y_std[counter] = np.std(old_image[0:75,0:75])
                 y_peak[counter] = old_image.max()
                 counter = counter + 1

             #print "x = ",x
             #print "y_std = ",y_std
             #print "y_peak = ",y_peak
             #print "y_std/y_peak = ",y_peak/y_std

             plt.plot(x,8.5*y_std,'ro')
             #plt.show()

             plt.plot(x,y_peak,'bo')
             plt.show()

             #plt.plot(x,y_peak/y_std,'go')

             #plt.plot(np.sort(x),y_10,"r")
            
             plt.show()
             os.chdir(it.PATH_CODE)

def main(argv):
   red_object = redpipe()
   flagallbasic = False
   bandpassgc = False
   plotcalgc = False
   applycalgcall = False
   createimages = False
   converttofits = False
   flagao = False
   mask1 = "C"
   mask2 = "C"
   delay = False
   decon = False

   try:
      opts, args = getopt.getopt(argv,"hd",["flag_all_basic","flag_ao","bandpass_gc","plot_cal_gc","apply_cal_gc_all","create_images=","print_lst","convert_to_fits=","decon_mask"])
   except getopt.GetoptError:
      print 'python redpipe.py -d --flag_all_basic --flag_ao --bandpass_gc --plot_cal_gc --apply_cal_gc_all --create_images <value> --print_lst --convert_to_fits <value> --decon_mask'
      sys.exit(2)
   for opt, arg in opts:
      #print "opt = ",opt
      #print "arg = ",arg
      if opt == '-h':
         print 'python redpipe.py -d --flag_all_basic --bandpass_gc --plotcal_gc --apply_cal_gc_all --create_images --print_lst --convert_to_fits --decon_mask'
         print '-d: adds a delay calibration step before the bandpass'
         print '--flag_all_basic: flag known bad channels, autocorrelations and antenna'
         print '--flag_ao: flag with ao flagger using strategy zen.2457545.48707.xx_strategy.rfis'
         print '--bandpass_gc: do a bandpass calibration on the snapshot where the galactic center is at zenith'
         print '--plot_cal_gc: plot the calibration bandpass solution obtained from doing a bandpass cal on the ms where gc is at zenith'
         print '--apply_cal_gc_all: apply the bandpass solutions obtained to all the other measurement sets in the directory'
         print '--create_images <value>: call clean and viewer to create some basic images (U - uncalibrated fluxscale, C - calibrated)' 
         print '--print_lst: converts the file names to lst and prints them'
         print '--convert_to_fits <value>: convert .image files to .fits (U - uncalibrated fluxscale, C - calibrated)'
         print '--decon_mask: create a decon mask'
         print "REMEMBER THAT HSA7458_V000_HH.PY AND CREATE_PS.PY HAS TO BE IN YOUR DATA DIRECTORY"
         sys.exit()
      elif opt == '-d':
           delay = True
      elif opt == "--flag_all_basic":
           flagallbasic = True
      elif opt == "--flag_ao":
           flagao = True
      elif opt == "--bandpass_gc":
           bandpassgc = True   
      elif opt == "--plot_cal_gc":
           plotcalgc = True
      elif opt == "--apply_cal_gc_all":
           applycalgcall = True
      elif opt == "--create_images":
           createimages = True
           if arg == "U":
              mask1 = "U"
      elif opt == "--convert_to_fits":
           #print "HALLO"
           converttofits = True
           if arg == "U":
              mask2 = "U"
      elif opt == "--print_lst":
	   msname = red_object.print_lst(print_values=True)
           print "Final MS: ",msname
      elif opt == "--decon_mask":
           #print "HALLO"
           decon = True

   if flagallbasic:
      red_object.flag_basic_all()
   if flagao:
      red_object.flag_aoflagger()
   if bandpassgc:
      red_object.bandpass_gc(delay=delay)
   if plotcalgc:
      red_object.plot_cal_gc(delay=delay)
   if applycalgcall:
      red_object.applycal_gc_all(delay=delay)
   if decon:
      #print "HALLO 2"
      red_object.produce_decon_mask()
   if createimages:
      red_object.create_images(mask = mask1)
   if converttofits:
      red_object.convert_to_fits(mask = mask2)
   
    		
if __name__ == "__main__":
   main(sys.argv[1:])
   #red_object = redpipe()
   #red_object.plot_peak_sigma()
   #red_object.produce_decon_mask()
   #red_object.create_images(mask = "C")
   #red_object.convert_to_fits(mask = "C")
   #red_object.flag_basic_all()
   #print red_object.print_lst(print_values=True)
   #red_object.bandpass_gc()
   #red_object.plot_cal_gc()
   #red_object.applycal_gc_all()
   #red_object.create_images()
   #plot_object = plotutilities()


