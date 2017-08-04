import numpy as np
import pylab as plt
import glob, os
from pyrap.tables import table
import pickle
from ephem import *

#SETTING LOCATIONS TO ALL THE IMPORTANT SCRIPTS AND DATA FILES
##############################################################################################################
PATH_TO_ADD_UVWS = "/home/trienko/HERA/software/capo/dcj/scripts/add_uvws.py"
CAL_FILE = "hsa7458_v000_HH" 
PATH_TO_MIR_TO_FITS = "/usr/local/bin/miriad_to_uvfits.py"
PATH_TO_MIR_TO_FITS_RID = "/home/trienko/HERA/conference/code/miriad2uvfits.py"
#PATH_DATA = r"/media/trienko/Seagate Expansion Drive/HERA/data/2457661/"
#PATH_DATA = "/home/trienko/HERA/conference/data/2457661/"
#PATH_DATA = "/home/trienko/HERA/conference/data/SIM_DATA/"
PATH_DATA = "/home/trienko/HERA/conference/data/AOFLAGGER/"
PATH_CODE = "/home/trienko/HERA/conference/code/"
OBSTABLENAME = "/home/trienko/HERA/software/casa-release-4.7.1-el7/data/geodetic/Observatories/"
ANT_ID = np.array([80,104,96,64,53,31,65,88,9,20,89,43,105,22,81,10,72,112,97])
##############################################################################################################

#GENERAL CASA WRAPPER FUNCTION
def CASA_WRAPPER(task="plotms",options={}):
    file = open(task+"_script.py","w")
    file.write("default("+task+")\n")
    for key in options.keys():
        if isinstance(options[key], str):
           file.write(key+"=\'"+options[key]+"\'\n") 
        else:
           file.write(key+"="+str(options[key])+"\n")
    if task <> "viewer":#FOR SOME REASON INP ON VIEWER HANGS
       file.write("inp("+task+")\n")
    file.write("go("+task+")\n")
    file.close()     

##############################################################################################################
#CLASS CONTAINING ALL THE IMPORTANT INITIALIZATION TASKS FOR HERA-19 COMMISIONING

#For every .uvc file
#*******************
#1. Add uv-tracks to miriad data files using the add_uvws command
#2. Convert miriad to uvfits using the miriad_to_uvfits command
#3. Convert uvfits to ms using the importuvfits command
#4. Swap the antenna columns s.t. A1 < A2

#Once off ater installing CASA for the first time
#************************************************
#5. Add HERA to CASA's observatory table 
##############################################################################################################

class inittasks():

      def __init__(self):
          pass

      #####################################
      #CASA wrapper around split 
      #####################################
      def split_wrapper(self,options={}):
          CASA_WRAPPER(task="split",options=options)
          print os.getcwd()
          command = "casa -c split_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around fixvis 
      #####################################
      def fixvis_wrapper(self,options={}):
          CASA_WRAPPER(task="fixvis",options=options)
          print os.getcwd()
          command = "casa -c fixvis_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      #####################################
      #CASA wrapper around fixvis 
      #####################################
      def concat_wrapper(self,options={}):
          CASA_WRAPPER(task="concat",options=options)
          print os.getcwd()
          command = "casa -c concat_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      ##############################
      #Reading all files with the .uvc extension and running the add_uvws command to add uv_tracks to the miriad files
      ##############################
      def add_uv_tracks(self):
          os.chdir(PATH_DATA)
           
          for file in glob.glob("*.uvc"):
              command = "python " + PATH_TO_ADD_UVWS + " -C " + CAL_FILE +" "+ file
              print("CMD >>> "+command)
              os.system(command)

	  os.chdir(PATH_CODE)

      ##############################
      #Deleting the uvcU files (miriad files with uv-tracks added)
      ##############################
      def remove_uvcU(self):
          os.chdir(PATH_DATA)
          for file in glob.glob("*.uvcU"):
              command = "rm -r "+ file
              print("CMD >>> "+command)
              os.system(command)
          os.chdir(PATH_CODE)

      ##############################
      #converting uvcU files to uvfits (to run must be in sudo)
      ##############################
      def miriad_to_uvfits(self):
          os.chdir(PATH_DATA)
           
          for file in glob.glob("*.uvcU"):
              command = "python " + PATH_TO_MIR_TO_FITS +" "+ file
              print("CMD >>> "+command)
              os.system(command)

	  os.chdir(PATH_CODE)

      def miriad_to_uvfits_rid(self):
          command = "sudo python run_miriad2uvfits.py" 
          print("CMD >>> "+command)
          os.system(command)

      def uvfits_to_miriad(self):
          command = "sudo python run_uvfits2miriad.py" 
          print("CMD >>> "+command)
          os.system(command)

      ##############################
      #Deleting the uvfits files
      ##############################
      def remove_uvfits(self):
          os.chdir(PATH_DATA)
          for file in glob.glob("*.uvfits"):
              command = "rm -r "+ file
              print("CMD >>> "+command)
              os.system(command)
          os.chdir(PATH_CODE)

      ##############################
      #Deleting the ms files
      ##############################
      def remove_ms(self):
          os.chdir(PATH_DATA)
          for file in glob.glob("*.ms"):
              command = "rm -r "+ file
              print("CMD >>> "+command)
              os.system(command)
          os.chdir(PATH_CODE)

      ##############################
      #Adding HERA to CASA's observatory table
      ##############################
      def add_HERA_observatory(self):
          file = open("add_HERA.py","w") 
          file.write("from casa import table as tb\n") 
          file.write("obstablename="+'"'+OBSTABLENAME+'"'+"\n") 
          file.write("tb.open(obstablename,nomodify=False)\n") 
          file.write("paperi =(tb.getcol(\"Name\")==\"PAPER_SA\").nonzero()[0]\n") 
          file.write("tb.copyrows(obstablename,startrowin=paperi,startrowout=-1,nrow=1)\n")
          file.write("tb.putcell(\"Name\",tb.nrows()-1,\"HERA\")\n")
          file.write("tb.close()\n")
          file.close() 
          command = "casa -c add_HERA.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command)
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      ##############################
      #Converting uvfits to ms
      ##############################
      def uv_fits_to_ms(self):
          os.chdir(PATH_DATA)
          for file_name in glob.glob("*U.uvfits"):
              file = open("uvfits_to_ms.py","w")
              msname = file_name[:-7]+".ms"
              file.write("default(importuvfits)\n")
              file.write("fitsfile=\""+file_name+"\"\n")
              file.write("vis=\""+msname+"\"\n")
              file.write("inp(importuvfits)\n")
              file.write("go(importuvfits)\n")
              file.close() 
              command = "casa -c uvfits_to_ms.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
              #break
          
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)
          os.chdir(PATH_CODE)

      ##############################
      #Converting ms to uvfits
      ##############################
      def ms_to_uv_fits(self):
          os.chdir(PATH_DATA)
          for file_name in glob.glob("*C.ms"):
              file = open("ms_to_uvfits.py","w")
              fits_file = file_name[:-3]+".uvfits"
              file.write("default(exportuvfits)\n")
              file.write("fitsfile=\""+fits_file+"\"\n")
              file.write("vis=\""+file_name+"\"\n")
              file.write("inp(exportuvfits)\n")
              file.write("go(exportuvfits)\n")
              file.close() 
              command = "casa -c ms_to_uvfits.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
              #break
          
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)
          os.chdir(PATH_CODE)

      def create_time_pickle(self):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*uvcU.ms")
          for file_name in file_names:
              t=table(file_name)
              time = t.getcol("TIME")
              #print "time = ",np.array(time)
              #print "len(time) = ",len(time)
              time2 = np.roll(time,1)
              time2[0] = time[0]
              dt = time-time2
              dt = dt[dt>1e-12]
              start_time = time - dt[0]/3.0
              end_time = time + dt[0]/3.0
              output = open(file_name[:-3]+".time.p",'wb')
              pickle.dump(start_time, output)
              pickle.dump(end_time, output)
              pickle.dump(time,output)
              output.close()
              #print "dt = ",len(dt[dt>1e-12])
              #plt.plot(dt)
              #plt.show()

          os.chdir(PATH_CODE)

      def compute_time_str(self):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*time.p")
          for file_name in file_names:
              file = open("time_str.py","w")

	      #file.write("def time_convert(mytime, myunit='s'):\n")
              #file.write("if type(mytime).__name__ <> 'list': mytime=[mytime]\n")
              #file.write("myTimestr = []\n")
              #file.write("for time in mytime:\n")
              #file.write("q1=qa.quantity(time,myunit)\n")
              #file.write("time1=qa.time(q1,form='ymd')\n")
              #file.write("myTimestr.append(time1)\n")
              #file.write("\n")
              #file.write("\n")
              #file.write("return myTimestr\n")
              #file.write("\n")
             
              file.write("import pickle\n")    
              file.write("execfile(\'time_func.py\')\n")
              file.write("from casa import table as tb\n")
              file.write("input = open(\""+file_name+"\",\'rb\')\n")
              file.write("time_start = pickle.load(input)\n")
              file.write("time_end = pickle.load(input)\n")
              file.write("time = pickle.load(input)\n")
              file.write("input.close()\n")
              file.write("time_start_str = time_convert(time_start)\n")
              file.write("time_end_str = time_convert(time_end)\n")
              file.write("time = time_convert(time)\n")
              file.write("output = open(\""+file_name[:-2]+".str.p\",\'wb\')\n")
              file.write("pickle.dump(time_start_str,output)\n")
	      file.write("pickle.dump(time_end_str,output)\n")
              file.write("pickle.dump(time,output)\n")
              file.write("output.close()\n")
              #file.write("print time_start_str\n")
              #file.write("print time_end_str\n")
              #file.write("tb.close()\n")
              file.close()
              command = "casa -c time_str.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
              #break
          os.chdir(PATH_CODE)

      def split_and_unphase_ms(self,unphase=True):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*uvcU.ms")
          #file_names = glob.glob("*time.str.p")
          for file_name in [file_names[0]]: 
              print "file_name = ",file_name
              input = open(file_name[:-3]+".time.str.p",'rb')
              start_str = pickle.load(input)
              end_str = pickle.load(input)
              time = pickle.load(input)
              input.close()
              start_str = np.unique(np.squeeze(np.array(start_str)))
              end_str = np.unique(np.squeeze(np.array(end_str)))
              time = np.unique(np.squeeze(np.array(time)))
              vis_list = []
              for k in xrange(len(start_str)):
                  options={}
                  options["vis"]=file_name
                  options["outputvis"]=file_name[:-3]+str(k)+".ms"
                  options["timerange"]=start_str[k]+"~"+end_str[k]
                  #self.split_wrapper(options=options)

                  if unphase:
                     options={}
                     options["vis"]=file_name[:-3]+str(k)+".ms"
                     options["outputvis"]=file_name[:-3]+str(k)+".ms"
                     vis_list.append(file_name[:-3]+str(k)+".ms")
                     HERA = Observer()
                     HERA.lat, HERA.long, HERA.elevation = '-30:43:17', '21:25:40.08', 0.0 
                     time_temp = time[k]
                     t_str = time_temp.split("/")
                     #print "t_str = ",t_str
                     HERA.date = t_str[0]+"/"+t_str[1]+"/"+t_str[2]+" "+t_str[3]
                     sid_str = str(HERA.sidereal_time())
                     sid_str_split = sid_str.split(":")
                     fix_vis_str = sid_str_split[0]+"h"+sid_str_split[1]+"m"+str(int(round(float(sid_str_split[2]))))+"s"
                     print sid_str_split
                     print time[k]
                     print "HERA.sidereal_time() = ",str(HERA.sidereal_time())
                     print fix_vis_str
                     
                     options["phasecenter"]='J2000 '+fix_vis_str+' -30d43m17s'
                     #self.fixvis_wrapper(options=options)
                     
              print "vis_list = ",vis_list 
              options={}
              options["vis"] = vis_list
              options["concatvis"] = file_name[:-3]+"P.ms"
              options["dirtol"] ="720arcmin"                  
              self.concat_wrapper(options=options)
                 
                  
          
          os.chdir(PATH_CODE)

      #def rephase_time_slots(self):
          

      def apply_flags(self):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*uvcU.ms")
          for file_name in file_names:
              file = open("apply_flags.py","w")
              file.write("from casa import table as tb\n") 
              file.write("tb.open(\""+file_name+"\",nomodify=False)\n")
              #file.write("flags = tb.getcol(\"FLAG\")\n")
              #file.write("flag_row = tb.getcol(\"FLAG_ROW\")\n")
              file.write("import pickle\n")
              file.write("input = open(\""+file_name[:-3]+".flags.p"+"\",\'rb\')\n")
              file.write("flags = pickle.load(input)\n")
              file.write("flag_row = pickle.load(input)\n")
              file.write("input.close()\n")
              file.write("tb.putcol(\"FLAG\",flags)\n")
              file.write("tb.putcol(\"FLAG_ROW\",flag_row)\n")
              file.write("tb.flush()\n")
              file.write("tb.close()\n")
              file.close()
              command = "casa -c apply_flags.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
              #break
          os.chdir(PATH_CODE)

      ##############################
      #Swap ANTENNA columns s.t. A1 < A2 
      ##############################  
      def swap_antenna(self):
          os.chdir(PATH_DATA)
          
          for file_name in glob.glob("*.ms"):
              file = open("swap.py","w")
              file.write("from casa import table as tb\n") 
              file.write("tb.open(\""+file_name+"\",nomodify=False)\n")
              file.write("a1,a2,data,uvw = [tb.getcol(x) for x in [\"ANTENNA1\",\"ANTENNA2\",\"DATA\",\"UVW\"]]\n")
              file.write("m = a1 > a2\n")
              file.write("data[:,:,m] = data[:,:,m].conj()\n")
              file.write("print data[:,:,m]\n")
              file.write("uvw[:,m] = (-1)*uvw[:,m]\n")
              file.write("x = a2[m]\n")
              file.write("a2[m] = a1[m]\n")
              file.write("a1[m] = x\n")
              file.write("tb.putcol(\"ANTENNA1\",a1)\n")
              file.write("tb.putcol(\"ANTENNA2\",a2)\n")
              file.write("tb.putcol(\"DATA\",data)\n")
              file.write("tb.putcol(\"UVW\",uvw)\n")
              file.write("tb.flush()\n")
              file.write("tb.close()\n")
              file.close()
              command = "casa -c swap.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
     
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)
          os.chdir(PATH_CODE)
              
      #def test_sudo(self):
      #    command = "sudo man"
      #    print("CMD >>> "+command)
      #    os.system(command)

                 

if __name__ == "__main__":
   #I NEED TO BE SUDO TO RUN THIS TASK WHICH IS WHY I HAVE WRITTEN A WRAPPER AROUND THIS CLASS WHICH CAN CALL THIS PYTHON FILE
   inittasks_object = inittasks()
   inittasks_object.miriad_to_uvfits()


   

