import numpy as np
import pylab as plt
import glob, os

#SETTING LOCATIONS TO ALL THE IMPORTANT SCRIPTS AND DATA FILES
##############################################################################################################
PATH_TO_ADD_UVWS = "/home/trienko/HERA/software/capo/dcj/scripts/add_uvws.py"
CAL_FILE = "hsa7458_v000_HH" 
PATH_TO_MIR_TO_FITS = "/usr/local/bin/miriad_to_uvfits.py"
PATH_DATA = "/home/trienko/HERA/conference/data/"
PATH_CODE = "/home/trienko/HERA/conference/code/"
OBSTABLENAME = "/home/trienko/HERA/software/casa-release-4.7.1-el7/data/geodetic/Observatories/"
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
          for file_name in glob.glob("*.uvfits"):
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
      #Swap ANTENNA columns s.t. A1 < A2 
      ##############################  
      def swap_antenna(self):
          os.chdir(PATH_DATA)
          
          for file_name in glob.glob("*.ms"):
              file = open("swap.py","w")
              file.write("from casa import table as tb\n") 
              file.write("tb.open(\""+file_name+"\",nomodify=False)\n")
              file.write("a1,a2,data = [tb.getcol(x) for x in [\"ANTENNA1\",\"ANTENNA2\",\"DATA\"]]\n")
              file.write("m = a1 > a2\n")
              file.write("data[:,:,m] = data[:,:,m].conj()\n")
              file.write("x = a2[m]\n")
              file.write("a2[m] = a1[m]\n")
              file.write("a1[m] = x\n")
              file.write("tb.putcol(\"ANTENNA1\",a1)\n")
              file.write("tb.putcol(\"ANTENNA2\",a2)\n")
              file.write("tb.putcol(\"DATA\",data)\n")
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


   

