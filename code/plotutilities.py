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

      def plot_auto_correlations_all(self,add_desc=""):
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

          if not os.path.isdir(FIGURE_PATH+"AUTO/"):
             command = "mkdir "+FIGURE_PATH+"AUTO/"
             print("CMD >>> "+command)
             os.system(command) 

          for file_name in glob.glob("*.ms"):
              options["vis"]=file_name
              options["plotfile"]=FIGURE_PATH+"AUTO/"+file_name[:-3]+'_AUTO'+add_desc+'.png'

              self.plotms_wrapper(options=options)
    
          os.chdir(it.PATH_CODE)

      def plot_hex_grid(self,flagged_ant=np.array([80,105,112]),plot_id=True,add_desc=""):
                   
          if plot_id:
             fig_name = "HEX19_ID"+add_desc+".png"
          else:
	     fig_name = "HEX19_NAME"+add_desc+".png"

          os.chdir(it.PATH_DATA)
          ant = self.hex_grid(hex_dim=2,l=20)
          plt.plot(ant[:,0],ant[:,1],'bo')
          ant_id = np.array([80,104,96,64,53,31,65,88,9,20,89,43,105,22,81,10,72,112,97])   
          
          if not plot_id:
             ant_id = ant_id + 1

          for label,x,y in zip(ant_id,ant[:,0],ant[:,1]):
       	      plt.annotate(str(label), xy = (x, y), xytext = (-5, -1), textcoords = 'offset points', fontsize = 10, ha = 'right', va = 'bottom')

          for flag_ant_value in flagged_ant:
              indx = np.where(ant_id == flag_ant_value)
              plt.plot(ant[indx,0],ant[indx,1],'ro')
          
          plt.xticks([])
          plt.yticks([])

          if not os.path.isdir(FIGURE_PATH+"LAYOUT/"):
             command = "mkdir "+FIGURE_PATH+"LAYOUT/"
             print("CMD >>> "+command)
             os.system(command) 

          plt.axis("equal")
       
          plt.savefig(FIGURE_PATH+"LAYOUT/"+fig_name)

      '''
      Generates an hexagonal layout
      
      RETURNS:
      None

      INPUTS:
      hex_dim - The amount of rings in the hexagonal layout
      l - Basic spacing between antennas
      ''' 
      def hex_grid(self,hex_dim,l):
          hex_dim = int(hex_dim)
          side = int(hex_dim + 1)
          ant_main_row = int(side + hex_dim)
        
          elements = 1

          #SUMMING ANTENNAS IN HEXAGONAL RINGS 
          for k in xrange(hex_dim):
              elements = elements + (k+1)*6
          
          #CREATING HEXAGONAL LAYOUT STARTING FROM CENTER      
          ant_x = np.zeros((elements,),dtype=float)
          ant_y = np.zeros((elements,),dtype=float)
          
          x = 0.0
          y = 0.0

          counter = 0
        
          for k in xrange(side):
              x_row = x
              y_row = y
              for i in xrange(ant_main_row):
                  if k == 0:
                     ant_x[counter] = x_row 
                     ant_y[counter] = y_row
                     x_row = x_row + l
                     counter = counter + 1 
                  else:
                     ant_x[counter] = x_row
                     ant_y[counter] = y_row
                     counter = counter + 1
                   
                     ant_x[counter] = x_row
                     ant_y[counter] = -1*y_row
                     x_row = x_row + l
                     counter = counter + 1   
              x = x + l/2.0
              y = y + (np.sqrt(3)/2.0)*l                 
              ant_main_row = ant_main_row - 1
       
          #RESORTING ANTENNA INDICES SO THAT LOWER LEFT CORNER BECOMES THE FIRST ANTENNA
          y_idx = np.argsort(ant_y)
          ant_y = ant_y[y_idx]
          ant_x = ant_x[y_idx]

          slice_value = int(side)
          start_index = 0
          add = True
          ant_main_row = int(side + hex_dim)

          for k in xrange(ant_main_row):
              temp_vec_x = ant_x[start_index:start_index+slice_value]
              x_idx = np.argsort(temp_vec_x)
              temp_vec_x = temp_vec_x[x_idx]
              ant_x[start_index:start_index+slice_value] = temp_vec_x
              if slice_value == ant_main_row:
                 add = False
              start_index = start_index+slice_value 
            
              if add:
                 slice_value = slice_value + 1
              else:
                 slice_value = slice_value - 1  

          #SHIFTING CENTER OF ARRAY TO ORIGIN
          max_x = np.amax(ant_x)
                    
          ant_x = ant_x - max_x/2.0
          
          temp_ant = np.zeros((len(ant_x),3),dtype=float)
          temp_ant[:,0] = ant_x
          temp_ant[:,1] = ant_y
          return temp_ant




if __name__ == "__main__":
   plot_object = plotutilities()
   #plot_object.plot_auto_correlations_all()
   plot_object.plot_hex_grid()
