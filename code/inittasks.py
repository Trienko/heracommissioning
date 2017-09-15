import numpy as np
import pylab as plt
import glob, os
from pyrap.tables import table
import pickle
from ephem import *
import getopt
import sys


#SETTING LOCATIONS TO ALL THE IMPORTANT SCRIPTS AND DATA FILES
##############################################################################################################
PATH_TO_ADD_UVWS = "/home/tlgrobler/software/capo/dcj/scripts/add_uvws.py"
CAL_FILE = "hsa7458_v001" 
PATH_TO_MIR_TO_FITS = "/usr/local/bin/miriad_to_uvfits.py"
PATH_TO_MIR_TO_FITS_RID = "/home/trienko/HERA/conference/code/miriad2uvfits.py"
#PATH_DATA = r"/media/trienko/Seagate Expansion Drive/HERA/data/2457661/"
PATH_DATA = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/TEST_PIPE/"
#PATH_DATA = "/home/trienko/HERA/conference/data/IMG/"
#PATH_DATA = "/home/trienko/HERA/conference/data/KWAZI/"
PATH_CODE = "/home/tlgrobler//heracommissioning/code/"
OBSTABLENAME = "/home/trienko/HERA/software/casa-release-4.7.1-el7/data/geodetic/Observatories/"
ANT_ID = np.array([80,104,96,64,53,31,65,88,9,20,89,43,105,22,81,10,72,112,97])
#SPEC_GC_DIR = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/"
SPEC_GC_DIR = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/TEST_PIPE/"
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
          print "PATH_DATA = ",PATH_DATA
           
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

      def set_PATH_DATA(self,path_data):
          global PATH_DATA
          PATH_DATA = path_data

      def create_time_pickle_N(self,N=56):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*U.ms")
          for file_name in file_names:
              t=table(file_name)
              time = t.getcol("TIME")
              #print "time = ",np.array(time)
              #print "len(time) = ",len(time)
              time2 = np.roll(time,1)
              time2[0] = time[0]
              dt = time-time2
              #print "time_before = ",time
              #print "time2_before = ",time2 
              #print "time[-1] = ",time[-1]
                
              time = time[dt>1e-12]
              time2 = time2[dt>1e-12]

              time2 = time2[::N]

              #print "time_after = ",time
              #print "time2_after = ",time2 
              #print "time[-1] = ",time[-1]
              #print "time2[-1] = ",time2[-1]
              #print "d = ",time-time2

              dt = dt[dt>1e-12]
              start_time = time2
              end_time = time2
              end_time = end_time[1:]
              final_end_time = np.array([time[-1]])
              end_time = np.append(end_time,final_end_time)
              output = open(file_name[:-3]+".time.N.p",'wb')
              #print "start_time = ",start_time
              #print "end_time = ",end_time
              #print "time = ",time
              pickle.dump(start_time, output)
              pickle.dump(end_time, output)
              pickle.dump(time2,output)
              pickle.dump(final_end_time,output)
              #output.close()
              #print "dt = ",len(dt[dt>1e-12])
              #plt.plot(dt)sys.argv[1:]
              #plt.show()

          os.chdir(PATH_CODE)

      def compute_time_str_N(self):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*time.N.p")
          for file_name in file_names:
              file = open("time_str_N.py","w")

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
              file.write("time_f = pickle.load(input)\n")
              file.write("input.close()\n")
              file.write("time_start_str = time_convert(time_start)\n")
              file.write("time_end_str = time_convert(time_end)\n")
              file.write("time = time_convert(time)\n")
              file.write("time_f = time_convert(time_f)\n")
              file.write("output = open(\""+file_name[:-2]+".str.p\",\'wb\')\n")
              file.write("pickle.dump(time_start_str,output)\n")
	      file.write("pickle.dump(time_end_str,output)\n")
              file.write("pickle.dump(time,output)\n")
              file.write("pickle.dump(time_f,output)\n")
              file.write("output.close()\n")
              #file.write("print time_start_str\n")
              #file.write("print time_end_str\n")
              #file.write("tb.close()\n")
              file.close()
              command = "casa -c time_str_N.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
              #break
          os.chdir(PATH_CODE)

      def split_and_unphase_ms_N(self,unphase=True):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*U.ms")
          #file_names = glob.glob("*time.str.p")
          for file_name in [file_names[0]]: 
              print "file_name = ",file_name
              input = open(file_name[:-3]+".time.N.str.p",'rb')
              start_str = pickle.load(input)
              end_str = pickle.load(input)
              time = pickle.load(input)
              time_f = pickle.load(input)
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
                  options["datacolumn"]="data"
                  self.split_wrapper(options=options)

                  print "start_str[k] = ",start_str[k]
                  print "end_str[k] = ",end_str[k]
                  print "k = ",k

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
                     self.fixvis_wrapper(options=options)
                     
              #print "vis_list = ",vis_list 
              options={}
              options["vis"] = vis_list
              options["concatvis"] = file_name[:-3]+"P.ms"
              options["dirtol"] ="720arcmin"                  
              #self.concat_wrapper(options=options)
                 
                  
          
          os.chdir(PATH_CODE)

      def create_time_pickle(self):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*U.ms")
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
              #print "start_time = ",start_time
              #print "end_time = ",end_time
              #print "time = ",time
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
      
      def create_t0_pickle(self):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*.tmp*")
          for file_name in file_names:
              if file_name[-2:] <> ".p":
                 t=table(file_name)
                 time = t.getcol("TIME")
                 t.close()
                 output = open(file_name+".time.p",'wb')
                 pickle.dump(np.array([time[0]]), output)
                 output.close()
          os.chdir(PATH_CODE)

      def compute_t0_str(self):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*time.p")
          for file_name in file_names:
              file = open("time_str.py","w")
              file.write("import pickle\n")    
              file.write("execfile(\'time_func.py\')\n")
              file.write("input = open(\""+file_name+"\",\'rb\')\n")
              file.write("t0 = pickle.load(input)\n")
              file.write("input.close()\n")
              file.write("t0_str = time_convert(t0)\n")
              file.write("output = open(\""+file_name[:-2]+".str.p\",\'wb\')\n")
              file.write("pickle.dump(t0_str,output)\n")
              file.write("output.close()\n")
              file.close()
              command = "casa -c time_str.py --nogui --nologfile --log2term"
              print("CMD >>> "+command)
              os.system(command)
          os.chdir(PATH_CODE)

      def rename_rephase_split_ms(self,rephase=True):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*.tmp*")
          for file_name in file_names:
              if file_name[-2:] <> ".p":
                 input = open(file_name+".time.str.p",'rb')
                 t0_str = pickle.load(input)[0][0]
 
                 print "t0_str = ",t0_str
                 
                 HERA = Observer()
                 HERA.lat, HERA.long, HERA.elevation = '-30:43:17', '21:25:40.08', 0.0 
                 j0 = julian_date(0)

                
                 t_str = t0_str.split("/")
                 HERA.date = t_str[0]+"/"+t_str[1]+"/"+t_str[2]+" "+t_str[3]
                 print file_name
                 print HERA.date     

                 sid_str = str(HERA.sidereal_time())
                 print "sid_str =",sid_str


                 sid_str_split = sid_str.split(":")
                 fix_vis_str = sid_str_split[0]+"h"+sid_str_split[1]+"m"+str(int(round(float(sid_str_split[2]))))+"s"
                 print "fix_vis =",fix_vis_str
                 HERA_date_str = '{:<013}'.format(float(HERA.date)+j0)
                 new_file_name = "zen."+HERA_date_str+".xx.HH.S.uvcU.ms"                 
                 command = "mv "+file_name+" "+new_file_name
                 print("CMD >>> "+command)
                 os.system(command)
                 if rephase:
                    options={}
                    options["vis"]=new_file_name
                    options["outputvis"]=new_file_name
                    options["phasecenter"]='J2000 '+fix_vis_str+' -30d43m17s'
                    self.fixvis_wrapper(options=options)

          os.chdir(PATH_CODE)
                 

      def split_sim_ms(self,ms_file,dummy_ms="dummy.ms",column="DATA",L=30):
          os.chdir(PATH_DATA)

          dummy_t=table(dummy_ms)
          dummy_data = dummy_t.getcol(column)
          dummy_ant1 = dummy_t.getcol("ANTENNA1")
          dummy_ant2 = dummy_t.getcol("ANTENNA2")
          dummy_uvw = dummy_t.getcol("UVW")
          dummy_time = dummy_t.getcol("TIME")
          dummy_flagrow = dummy_t.getcol("FLAG_ROW")
          dummy_t.close()

          ts = (dummy_data.shape[0])/L
          chan = dummy_data.shape[1] 

          t = table(ms_file)
          data = t.getcol(column)
          ant1 = t.getcol("ANTENNA1")
          ant2 = t.getcol("ANTENNA2")
          uvw = t.getcol("UVW")
          time = t.getcol("TIME")
          flagrow = t.getcol("FLAG_ROW")
          t.close()                 

          not_finished = True

          l = 0
          h = ts*L
          
          dl = 0
          dh = ts*L

          counter = 0

          while not_finished:
                              
                if h > data.shape[0]:
                   h = data.shape[0]
                   dh = h - l
                   dummy_flagrow[dh:] = True
                   not_finished = False

                new_dummy = dummy_ms + ".tmp" + str(counter)

                command = "cp -r " + dummy_ms + " " + new_dummy 
                print("CMD >>> "+command)
                os.system(command) 
                
                #print "counter = ",counter 
                #print "l = ",l
                #print "h = ",h

                dummy_data[dl:dh,:,:] = data[l:h,:,:]
                dummy_ant1[dl:dh] = ant1[l:h]
                dummy_ant2[dl:dh] = ant2[l:h]
                dummy_uvw[dl:dh,:] = uvw[l:h,:]
                dummy_time[dl:dh] = time[l:h]
                dummy_flagrow[dl:dh] = flagrow[l:h]
                
                dummy_t=table(new_dummy,readonly=False)
                dummy_t.putcol(column,dummy_data) 
                dummy_t.putcol("ANTENNA1",dummy_ant1)
                dummy_t.putcol("ANTENNA2",dummy_ant2)
                dummy_t.putcol("UVW",dummy_uvw)
                dummy_t.putcol("TIME",dummy_time)
                dummy_t.putcol("FLAG_ROW",dummy_flagrow) 
                 
                dummy_t.close()             
                
                l += ts*L
                h += ts*L
                counter += 1
          
          #print "ts = ",ts
          #print "chan = ",chan
          
          os.chdir(PATH_CODE)

      def split_and_unphase_ms(self,unphase=True):
          os.chdir(PATH_DATA)
          file_names = glob.glob("*U.ms")
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

                  print "start_str[k] = ",start_str[k]
                  print "end_str[k] = ",end_str[k]
                  print "k = ",k

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
                     
              #print "vis_list = ",vis_list 
              options={}
              options["vis"] = vis_list
              options["concatvis"] = file_name[:-3]+"P.ms"
              options["dirtol"] ="720arcmin"                  
              #self.concat_wrapper(options=options)
                 
                  
          
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
   argv = sys.argv[1:]
   inittasks_object = inittasks()
   
   #I NEED TO BE SUDO TO RUN THIS TASK WHICH IS WHY I HAVE WRITTEN A WRAPPER AROUND THIS CLASS WHICH CAN CALL THIS PYTHON FILE   
   try:
      opts, args = getopt.getopt(argv,"h",["set_data_path="])
   except getopt.GetoptError:
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h': 
          print "WRAPPER"
       elif opt == "--set_data_path":
          inittasks_object.set_PATH_DATA(arg) 

   inittasks_object.miriad_to_uvfits()


   

