import numpy as np
import scipy as sp
import pylab as plt
import inittasks as it
import glob, os
import sys, getopt

#Figure path
######################################
FIGURE_PATH = it.PATH_DATA+'figures/'
######################################


######################################
#This class enables a lot of plotting

#1. Plotting autocorrelations
#2. Plotting redindant groups (per baseline or combined)
#3. Plotting HEX-19 with antenna labels (either ids or names)
######################################
class plotutilities():

      def __init__(self):
          pass


      def set_PATH_DATA(self,path_data):
          global FIGURE_PATH
          FIGURE_PATH = path_data+'figures/'
          inittasks_object = it.inittasks()
          inittasks_object.set_PATH_DATA(path_data)

      
      #####################################
      #CASA wrapper around the plotms task using the CASA_WRAPPER function from inittasks
      #####################################
      def plotms_wrapper(self,options={}):
          it.CASA_WRAPPER(task="plotms",options=options)
          print os.getcwd()
          command = "casa -c plotms_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      ######################################
      #Plot all autocorrelations of all the ms in the data directory using the plotms CASA task
      ######################################           
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

      ######################################
      #Plot all correlations of all the ms in the data directory using the plotms CASA task
      ######################################           
      def plot_cross_correlations_all(self,ymax = 6,add_desc=""):
          os.chdir(it.PATH_DATA)
          options={}          
          options["xaxis"]='freq'
          options["yaxis"]='amp'
          options["averagedata"]=True
          options["avgtime"]='1000'
          options["coloraxis"]='baseline'
          options["antenna"]='*&'
          options["expformat"]='png'
          options["showgui"]=False
          options["overwrite"]=True
          options["plotrange"]=[0,0,0,ymax]
         
          if not os.path.isdir(FIGURE_PATH):
             command = "mkdir "+FIGURE_PATH
             print("CMD >>> "+command)
             os.system(command)

          if not os.path.isdir(FIGURE_PATH+"CROSS/"):
             command = "mkdir "+FIGURE_PATH+"CROSS/"
             print("CMD >>> "+command)
             os.system(command) 

          for file_name in glob.glob("*.ms"):
              options["vis"]=file_name
              options["plotfile"]=FIGURE_PATH+"CROSS/"+file_name[:-3]+'_CROSS'+add_desc+'.png'

              self.plotms_wrapper(options=options)
    
          os.chdir(it.PATH_CODE)

      ######################################
      #Plot all the visibilities for all the redundant groups
      ######################################
      def plot_redundant_groups_all(self,add_desc="",ymax=6,per_baseline=False):
                  
          os.chdir(it.PATH_DATA)

          ant_id = np.copy(it.ANT_ID)
          
          ant = self.hex_grid(hex_dim=2,l=20) #GENERAT HEX-19 LAYOUT

          phi,zeta,L = self.calculate_phi(ant[:,0],ant[:,1])

          options={}          
          options["xaxis"]='freq'
          options["yaxis"]='amp'
          options["xdatacolumn"] = "corrected"
          options["ydatacolumn"] = "corrected"
          options["averagedata"]=True
          options["avgtime"]='1000'
          options["coloraxis"]='baseline'
          options["expformat"]='png'
          options["showgui"]=False
          options["overwrite"]=True
          options["plotrange"]=[0,0,0,ymax]
          if per_baseline:
             options["iteraxis"]="baseline"
             options["exprange"]="all"
             
          
          if not os.path.isdir(FIGURE_PATH+"REDUNDANT_GROUPS/"):
             command = "mkdir "+FIGURE_PATH+"REDUNDANT_GROUPS/"
             print("CMD >>> "+command)
             os.system(command) 

          for file_name in glob.glob("*.ms"): #LOOP THROUGH ALL MS FILES
              options["vis"]=file_name
              file_name_split = file_name.split('.')
              dirname = file_name_split[1]+'.'+file_name_split[2]
              
              if not os.path.isdir(FIGURE_PATH+"REDUNDANT_GROUPS/"+dirname+"/"):
            	 command = "mkdir "+FIGURE_PATH+"REDUNDANT_GROUPS/"+dirname+"/"
             	 print("CMD >>> "+command)
                 os.system(command) 

              for i in xrange(1,L+1): #LOOP THROUGH ALL REDUNDANT GROUPS
                  
                  options["plotfile"]=FIGURE_PATH+"REDUNDANT_GROUPS/"+dirname+"/"+file_name[:-3]+'_REG_'+str(i)+add_desc+'.png'
                  ant_str = ""
                  for k in xrange(len(ant[:,0])):
                      for j in xrange(k+1,len(ant[:,0])): #LOOP THROUGH ALL ANTENNA PAIRS  
                          if (phi[k,j] == i):
                             #if ant_id[k] < ant_id[j]: #IF YOU WANT TO CHANGE ANTENNA PAIRS S.T. A1<A2  
                             #   p = ant_id[k]
                             #   q = ant_id[j]
                             #else:
                             #   p = ant_id[j]
                             #   q = ant_id[k]
                             p = ant_id[k]+1 #TAKES ANT NAME NOT ID (NAME = ID + 1)
                             q = ant_id[j]+1 #SUBSTITUTE THE ID GIVEN BY HEX DIAGRAM ON HERA WIKI
                             ant_str = ant_str + str(p)+"&"+str(q)+";"
                  ant_str = ant_str[:-1]
                  options["antenna"]=ant_str
                  self.plotms_wrapper(options=options)
                  #self.plotms
          os.chdir(it.PATH_CODE)


      ######################################
      #Plot the 19 HEX HERA layout correctly numbering the antennas with id or name (name = id + 1) depending on the value of plot_id
      ######################################
      def plot_hex_grid(self,flagged_ant=np.array([]),plot_id=True,add_desc=""):
                   
          os.chdir(it.PATH_DATA)

          if plot_id:
             fig_name = "HEX19_ID"+add_desc+".png"
          else:
	     fig_name = "HEX19_NAME"+add_desc+".png"

          ant = self.hex_grid(hex_dim=2,l=20)
          plt.clf()
          plt.plot(ant[:,0],ant[:,1],'bo')
          ant_id = np.copy(it.ANT_ID) 
          
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
          os.chdir(it.PATH_CODE)


      ######################################
      #Generates the antenna positions for a hexagonal grid
      ######################################
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

      ######################################
      #Converts the antenna idices pq into a redundant index
      #   
      #INPUTS:
      #red_vec_x - the current list of unique redundant baseline vector (x-coordinate)
      #red_vec_y - the current list of unique redundant baseline vector (y-coordinate)
      #ant_x_p - the x coordinate of antenna p
      #ant_x_q - the x coordinate of antenna q
      #ant_y_p - the y coordinate of antenna p
      #ant_y_q - the y coordinate of antenna q
      #
      #RETURNS:
      #red_vec_x - the current list of unique redundant baseline vector (x-coordinate)
      #red_vec_y - the current list of unique redundant baseline vector (y-coordinate)
      #l - The redundant index associated with antenna p and q
      ######################################
      def determine_phi_value(self,red_vec_x,red_vec_y,ant_x_p,ant_x_q,ant_y_p,ant_y_q):
          red_x = ant_x_q - ant_x_p
          red_y = ant_y_q - ant_y_p

          for l in xrange(len(red_vec_x)):
              if (np.allclose(red_x,red_vec_x[l]) and np.allclose(red_y,red_vec_y[l])):
                 return red_vec_x,red_vec_y,int(l+1)

          red_vec_x = np.append(red_vec_x,np.array([red_x]))
          red_vec_y = np.append(red_vec_y,np.array([red_y]))
          return red_vec_x,red_vec_y,int(len(red_vec_x)) 

      ######################################
      #Returns the mapping phi, from pq indices to redundant indices.
      #INPUTS:
      #ant_x - vector containing the x-positions of all the antennas
      #ant_y - vector containing the y-positions of all the antennas 
      #
      #RETURNS:
      #phi - the mapping from pq indices to redundant indices
      #zeta - the symmetrical counterpart
      #L - maximum number of redundant groups  
      ######################################
      def calculate_phi(self,ant_x,ant_y):
          phi = np.zeros((len(ant_x),len(ant_y)),dtype=int)
          zeta = np.zeros((len(ant_x),len(ant_y)),dtype=int)
          red_vec_x = np.array([])
          red_vec_y = np.array([])
          for k in xrange(len(ant_x)):
              for j in xrange(k+1,len(ant_x)):
                  red_vec_x,red_vec_y,phi[k,j]  = self.determine_phi_value(red_vec_x,red_vec_y,ant_x[k],ant_x[j],ant_y[k],ant_y[j])           
                  zeta[k,j] = phi[k,j]
                  zeta[j,k] = zeta[k,j]
          L = np.amax(zeta)
          return phi,zeta,L

def main(argv):
   plot_object = plotutilities()
   plt_auto = False
   plt_red = False
   plt_lay = False   
   plot_id = False
   plt_cross = False
   per_baseline = False
   ymax = 6

   try:
      opts, args = getopt.getopt(argv,"harlc",["id_true=","ymax=","per_baseline="])
   except getopt.GetoptError:
      print 'python plotutilities.py -a -r -l -c --id_true <value> --per_baseline <value> --ymax <value>'
      sys.exit(2)
   for opt, arg in opts:
      #print "opt = ",opt
      #print "arg = ",arg
      if opt == '-h':
         print 'python plotutilities.py -a -r -l --per_baseline <value> --ymax <value> --id_true <value>'
         print '-a: plot all the autocorrelations for all the measurement sets in current directory'
         print '-r: plot all the correlations associated with the different baseline groups for all the measurement sets in current directory'
         print '-l: plot the HERA-19 layout with antenna labels'
         print '-c: plot all cross-correlations'
         print '--ymax <value>: (must be a real number) On the correlation plots this is the chosen maximum y-value. Default is 6.'
         print '--per_baseline <value>: (must be a boolean) Produce per-baseline correlation plots. Default is False.' 
         print '--id_true <value>: (must be a boolean) On the HERA-19 layout plot use CASA antenna names or HERA wiki ids. Default is False.'
         print "REMEMBER TO SET THE LOCATION OF WHERE THE FIGURES SHOULD BE STORED IN THE HEADER OF PLOTUTILITIES.PY"
         sys.exit()
      elif opt == "-a":
           plt_auto = True
      elif opt == "-r":
           plt_red = True
      elif opt == "-l":
           plt_lay = True
      elif opt == "--id_true":
           if arg == "True":
              plot_id = True
              print "plot_id = ",plot_id
      elif opt == "-c":
           plt_cross = True
      elif opt == "--ymax":
              ymax = float(arg)
              #print "ymax = ",ymax
      elif opt == "--per_baseline":
           if arg == "True":
              per_baseline = True
	      print "per_baseline = ",per_baseline

   if plt_auto:
      plot_object.plot_auto_correlations_all()
   if plt_red:
      #print "ymax2 = ",ymax
      plot_object.plot_redundant_groups_all(ymax=ymax,per_baseline=per_baseline)
   if plt_lay:
      plot_object.plot_hex_grid(plot_id=plot_id)
   if plt_cross:
      plot_object.plot_cross_correlations_all(ymax=ymax)

if __name__ == "__main__":
   main(sys.argv[1:])
   #plot_object = plotutilities()
   #plot_object.plot_auto_correlations_all()
   #plot_object.plot_hex_grid()

   #plot_object.plot_redundant_groups_all(per_baseline=True)
