from ephem import *
import numpy as np
import pylab as plt
import glob, os
import inittasks as it
import plotutilities as plutil

FLAG_SPW_STRING = '0:0~140;379~387;768~770;851~852;901~1023'
FLAG_ANT_STRING = '81;82;113'
SGR_STR = '17:45:40.0'
SGR_FLOAT = (17.0/24 + 45.0/60 + 40.0/3600)*(pi/12)
BANDBASS_GC_CAL_TABLE = ''
POINT_SOURCE_MODEL = 'point_source_model.cl'

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

      def print_lst(self,print_values=False):
          os.chdir(it.PATH_DATA)
          HERA = Observer()
          HERA.lat, HERA.long, HERA.elevation = '-30:43:17', '21:25:40.08', 0.0
          j0 = julian_date(0)

          file_names = glob.glob("*.ms")
          ra_cen = np.zeros((len(file_names),))
          k = 0        
 
          for file_name in file_names:
              file_name_split = file_name.split('.')
              lst = file_name_split[1]+'.'+file_name_split[2]
              HERA.date = float(lst) - j0
              ra_cen[k] = float(HERA.sidereal_time())
              k = k + 1
              if print_values:
                 print "MSNAME: %s, UTC: %s (LST %s = %f):" % (file_name, HERA.date, HERA.sidereal_time(), float(HERA.sidereal_time()) )
	      
          d = np.absolute(ra_cen - SGR_FLOAT)
          index_min = np.argmin(d)
          msname = file_names[index_min]
          #print msname
          os.chdir(it.PATH_CODE)
          return msname

      def bandpass_gc(self):
          global BANDBASS_GC_CAL_TABLE
          gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
          os.chdir(it.PATH_DATA)
          
          #CREAT POINT SOURCE MODEL AT THE POS OF GALACTIC CENTER
          if not os.path.isfile('point_source_model.cl'):
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
          
          BANDBASS_GC_CAL_TABLE = 'b_'+gc_jd+'.cal'

          #BANDPASS CALIBRTION OF GC-MS WITH PS AT GALACTIC CENTER
          options={}
          options["vis"]=gc_name
          options["solint"]='inf'
          options["combine"]='scan'
          options["caltable"] = BANDBASS_GC_CAL_TABLE 
          self.bandpass_wrapper(options=options)
          os.chdir(it.PATH_CODE)

      def plot_cal_gc(self):
          global BANDBASS_GC_CAL_TABLE
          if BANDBASS_GC_CAL_TABLE == '':
             gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
	     gc_name_split = gc_name.split('.')
             gc_jd = gc_name_split[1]+'.'+gc_name_split[2]
          
             BANDBASS_GC_CAL_TABLE = 'b_'+gc_jd+'.cal'
           
          os.chdir(it.PATH_DATA)
                       
          if os.path.isdir(BANDBASS_GC_CAL_TABLE):  
             if not os.path.isdir(plutil.FIGURE_PATH+"CAL_SOLUTIONS/"):
             	command = "mkdir "+plutil.FIGURE_PATH+"CAL_SOLUTIONS/"
             	print("CMD >>> "+command)
             	os.system(command)

             options={}
             options["caltable"]=BANDBASS_GC_CAL_TABLE
             options["xaxis"]='freq'
             options["yaxis"]='phase'
             options["showgui"]=False
             options["figfile"]=plutil.FIGURE_PATH+"CAL_SOLUTIONS/"+BANDBASS_GC_CAL_TABLE+"_PHASE.png"
	     self.plotcal_wrapper(options=options)

             options={}
             options["caltable"]=BANDBASS_GC_CAL_TABLE
             options["xaxis"]='freq'
             options["yaxis"]='amp'
             options["showgui"]=False
             options["figfile"]=plutil.FIGURE_PATH+"CAL_SOLUTIONS/"+BANDBASS_GC_CAL_TABLE+"_AMP.png"
	     self.plotcal_wrapper(options=options)
          os.chdir(it.PATH_CODE)

      def applycal_gc_all(self):
          global BANDBASS_GC_CAL_TABLE
          if BANDBASS_GC_CAL_TABLE == '':
             gc_name = self.print_lst(print_values=False) #print lst flips between code and data dir already needs to be placed first
	     gc_name_split = gc_name.split('.')
             gc_jd = gc_name_split[1]+'.'+gc_name_split[2]
          
             BANDBASS_GC_CAL_TABLE = 'b_'+gc_jd+'.cal'

          os.chdir(it.PATH_DATA)
          file_names = glob.glob("*.ms")
          for file_name in file_names:
              options={}
              options["vis"] = file_name
              options["gaintable"]=BANDBASS_GC_CAL_TABLE
	      self.applycal_wrapper(options=options)
          os.chdir(it.PATH_CODE)

      def create_images(self):
          os.chdir(it.PATH_DATA)
                       
          if not os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"):
             command = "mkdir "+plutil.FIGURE_PATH+"IMAGES/"
             print("CMD >>> "+command)
             os.system(command)

          file_names = glob.glob("*.ms")

          for file_name in file_names:
              
              if os.path.isdir(plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".model"):
                 command = "rm -r "+plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".*"
                 print("CMD >>> "+command)
                 os.system(command)

              #RUN THE CLEAN TASK
              options={}
              options["vis"] = file_name
              options["imagename"] = plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]
              options["imagermode"] = 'csclean'
              options["psfmode"] = 'clark'
              options["threshold"]='0.2Jy'
              options["niter"]=3
              options["mode"]='mfs'
              options["cell"]=['10arcmin','10arcmin']
              options["weighting"]='uniform'
              options["imsize"]=[240,240]
              options["gridmode"]='widefield'
              options["wprojplanes"]=128
              options["gain"]=0.2
              options["interactive"]=False

	      self.clean_wrapper(options=options)

              #RUN VIEWER
              options={}
              options["infile"] = plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".image"
              options["outfile"] = plutil.FIGURE_PATH+"IMAGES/"+file_name[:-3]+".png"
              options["outformat"] = 'png'
              options["gui"]=False
            
              self.viewer_wrapper(options=options)
          os.chdir(it.PATH_CODE)
       		
if __name__ == "__main__":
   #main(sys.argv[1:])
   red_object = redpipe()
   #red_object.flag_basic_all()
   #print red_object.print_lst(print_values=True)
   #red_object.bandpass_gc()
   #red_object.plot_cal_gc()
   #red_object.applycal_gc_all()
   red_object.create_images()
   
   #plot_object = plotutilities()


