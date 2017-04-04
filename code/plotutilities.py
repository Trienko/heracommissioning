import numpy as np
import scipy as sp
import pylab as plt
import inittasks as it
import glob, os

MS_NAME = "TEMP"
FIGURE_PATH = it.PATH_DATA+'figures/'

#plotms(vis='zen.2457545.48011.xx.HH.uvcU.ms',xaxis='freq',yaxis='amp',averagedata=True,avgtime='1000',coloraxis='baseline',antenna='*&&&')

class plotutilities():

      def __init__(self):
          pass

      def plotms_wrapper(self,options={}):
          os.chdir(it.PATH_DATA)
          it.CASA_WRAPPER(task="plotms",options=options)
          print os.getcwd()
          command = "casa -c plotms_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)
          os.chdir(it.PATH_CODE)

      def plot_auto_correlations_all(self):
          os.chdir(it.PATH_DATA)
          options={}          
          options["xaxis"]='freq'
          options["yaxis"]='amp'
          options["averagedata"]=True
          options["avgtime"]='1000'
          options["coloraxis"]='baseline'
          options["antenna"]='*&&&'
          options["expformat"]='png'
          options["showgui"]=False
          options["overwrite"]=True

          

          for file_name in glob.glob("*.ms"):
              options["vis"]=file_name
              options["plotfile"]=FIGURE_PATH+file_name[:-3]+'_AUTO.png'

              self.plotms_wrapper(options=options)
    
          os.chdir(it.PATH_CODE)


if __name__ == "__main__":
   plot_object = plotutilities()
   plot_object.plot_auto_correlations_all()

