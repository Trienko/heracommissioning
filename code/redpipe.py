from ephem import *
import numpy as np
import pylab as plt
import glob, os
import inittasks as it

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
          
if __name__ == "__main__":
   #main(sys.argv[1:])
   red_object = redpipe()
   print red_object.print_lst(print_values=True)
   red_object.bandpass_gc()
   #red_object.flag_basic_all()
   #plot_object = plotutilities()


