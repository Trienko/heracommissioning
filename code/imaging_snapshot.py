import numpy as np
import inittasks as it
from pyrap.tables import table
import os
import glob

#rad2deg = lambda val: val * 180./np.pi
#deg2rad = lambda val: val * np.pi/180

class imager():
      def __init__(self):
          pass

      #####################################
      #CASA wrapper around fixvis 
      #####################################
      def fixvis_wrapper(self,options={}):
          it.CASA_WRAPPER(task="fixvis",options=options)
          print os.getcwd()
          command = "casa -c fixvis_script.py --nogui --nologfile --log2term"
          print("CMD >>> "+command)
          os.system(command) 
          command = "rm ipython*.log"
          print("CMD >>> "+command)
          os.system(command)

      # converting ra and dec to l and m coordiantes
      def radec2lm(self,ra0,dec0,ra_r,dec_r):
          l = np.cos(dec_r)* np.sin(ra_r - ra0)
          m = np.sin(dec_r)*np.cos(dec0) - np.cos(dec_r)*np.sin(dec0)*np.cos(ra_r-ra0)
          return l,m #lm in radians


      def fix_vis_beam_creator(self,min_spacing=16,search_string="*C.ms",dec_shift="-30d43m17s"):
          file_names,ra_h,ra_m,l,m = self.create_dictionary_lm(min_spacing=min_spacing,search_string=search_string,dec_shift=dec_shift)
          
          #COPY OF MS
          '''
          for file_name in file_names:
              new_file_name = file_name[-3]+"F.ms"
              command = "cp - r "+file_name+" "+new_file_name
              print("CMD >>> "+command)
              os.system(command)
          '''
 
          k = 0
          for file_name in file_names:
              options["vis"]=file_name
              options["outputvis"]=file_name[:-3]+"F.ms"
              fix_vis_str = str(int(ra_h)) + "h" + str(int(ra_m)) + "m" 
              options["phasecenter"]='J2000 '+fix_vis_str+' '+dec_shift
              self.fixvis_wrapper(options) 
          

                                

      def create_dictionary_lm(self,min_spacing=16,search_string="*C.ms",dec_shift="-30d43m17s"):
          
          rad2deg = lambda val: val * 180./np.pi
          deg2rad = lambda val: val * np.pi/180

          os.chdir(it.PATH_DATA)
          hours_m_vec,minutes_m_vec,hours_vec,minutes_vec,h,hm = self.create_ph_center_hour_vec(min_spacing=min_spacing)
          
          file_names = glob.glob(search_string)
          ra_cen = np.zeros((len(file_names),))
          dec_cen = np.zeros((len(file_names),))
          ra_shift = np.zeros((len(file_names),))
          ra_h = np.zeros((len(file_names),))
          ra_m = np.zeros((len(file_names),))
          l = np.zeros((len(file_names),))
          m = np.zeros((len(file_names),))
          
          dec_split = dec_shift.split("d")
          d_str = dec_split[0]
          dec_split = dec_split[1].split("m")
          m_str = dec_split[0]
          s_str = dec_split[1]
          s_str = s_str[:-1]
          dec_shift = deg2rad(float(d_str)+float(m_str)/60 + float(s_str)/3600) 


          print "d_str = ",d_str
          print "s_str = ",s_str
          print "m_str = ",m_str

          k = 0

          for file_name in file_names:
              t=table(file_name+"/FIELD",readonly=False)
              phase_dir_ra = t.getcol("PHASE_DIR")[0][0][0] #in radians
              phase_dir_dec = t.getcol("PHASE_DIR")[0][0][1] #in radians
              
              if phase_dir_ra < 0:
                 phase_dir_ra = (phase_dir_ra+2*np.pi)

              ra_cen[k] = phase_dir_ra
              dec_cen[k] = phase_dir_dec 
              ra_shift[k] = hm[ra_cen[k]<h][0]
              ra_h[k] = hours_m_vec[ra_cen[k]<h][0]
              ra_m[k] = minutes_m_vec[ra_cen[k]<h][0]
              l[k],m[k] = self.radec2lm(ra_shift[k],dec_shift,ra_cen[k],dec_cen[k])
              k += 1
              #options["phasecenter"]='J2000 '+fix_vis_str+' -30d43m17s'
               

          #print "ra_cen = ",ra_cen
          #print "dec_cen = ",dec_cen
          #print "dec_shift = ",dec_shift
          #print "ra_shift = ",ra_shift
          #print "ra_h = ",ra_h
          #print "ra_m = ",ra_m  
          #print "h = ",h
          #print "l = ",l * 180./np.pi
          #print "m = ",m * 180./np.pi
              
          os.chdir(it.PATH_CODE)
          return file_names,ra_h,ra_m,l,m

      def create_ph_center_hour_vec(self,min_spacing=16):
          hours = 0
          hours_m = 0
          minutes = 0
          minutes_m = -1*(min_spacing/2)

          hours_vec = np.array([])
          minutes_vec = np. array([])

          hours_m_vec = np.array([])
          minutes_m_vec = np.array([])       

          while hours < 24:
              minutes += min_spacing
              if minutes >= 60:
                 minutes = minutes - 60
                 hours = hours + 1

              hours_vec = np.append(hours_vec,hours)
              minutes_vec =np.append(minutes_vec,minutes)
              #print "********************"
              #print "hours = ",hours
              #print "minutes = ",minutes
              #print "********************"

          while hours_m < 24:
                minutes_m = minutes_m + min_spacing
                if minutes_m >= 60:
                   minutes_m = minutes_m - 60
                   hours_m = hours_m + 1
                hours_m_vec = np.append(hours_m_vec,hours_m)
                minutes_m_vec = np.append(minutes_m_vec,minutes_m)                  
                #print "********************"
                #print "hours_m = ",hours_m
                #print "minutes = ",minutes_m
                #print "********************"

          hours_m_vec = hours_m_vec[:len(hours_vec)]
          minutes_m_vec = minutes_m_vec[:len(minutes_vec)]
 
          h = (hours_vec + (minutes_vec/60.0))*np.pi/12
          hm = (hours_m_vec + (minutes_m_vec/60.0))*np.pi/12 

          #print "hm = ",len(hours_m_vec)
          #print "mm = ",len(minutes_m_vec)
          #print "h = ",len(hours_vec)
          #print "m = ",len(minutes_vec)

          #print "hm = ",hours_m_vec
          #print "mm = ",minutes_m_vec
          #print "h = ",hours_vec
          #print "m = ",minutes_vec
          #print "h_r = ",h
          #print "hm_r = ",hm
          return hours_m_vec,minutes_m_vec,hours_vec,minutes_vec,h,hm

              
              

if __name__ == "__main__":
   img = imager()

   img.fix_vis_beam_creator() 

   #img.create_dictionary_lm()

   #img.create_ph_center_hour_vec(16)   
