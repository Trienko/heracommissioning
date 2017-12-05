import numpy as np
import inittasks as it
from pyrap.tables import table
import os
import glob
import stripe as s
import plotutilities as plutil
import pyfits

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


      def fix_vis_beam_creator(self,min_spacing=30,search_string="*C.ms",dec_shift="-30d43m17s"):#dec_shift="-30d43m17s"
          rad2deg = lambda val: val * 180./np.pi

          file_names,ra_h,ra_m,l,m,hours_m_vec,minutes_m_vec = self.create_dictionary_lm(min_spacing=min_spacing,search_string=search_string,dec_shift=dec_shift)
          
          os.chdir(it.PATH_DATA)

          print "file_names = ",file_names
          
          #COPY OF MS
          for file_name in file_names:
              #print "file_name[-3] = ",file_name[-3]
              new_file_name = file_name[:-3]+"F.ms"
              command = "cp -r "+file_name+" "+new_file_name
              print("CMD >>> "+command)
              os.system(command)

          
          #COPYING NEEDED PYTHON FILES
          files_python = np.array(["ClassMS_psa64.py","ModColor.py","ModRotate_psa64.py","rad2hmsdms.py","reallyFixVis_psa64.py","reformat.py",])

          for code_file in files_python:
              if not os.path.isfile(code_file):
                 command = "cp -r "+it.PATH_CODE+code_file+" ."
                 print("CMD >>> "+command)
                 os.system(command)  
          
          #USING REALLY FIXVIS
          k = 0
          dec_shift_r=dec_shift.replace("d",":")
          dec_shift_r=dec_shift_r.replace("m",":")
          dec_shift_r=dec_shift_r.replace("s","")
          dec_shift_r = dec_shift_r+".000"
          
          for file_name in file_names:
              ms = file_name[:-3]+"F.ms"
              ra_str = str(int(ra_h[k])) + ":" + str(int(ra_m[k])) + ":00.000"
              command = "python reallyFixVis_psa64.py --str --ra " + ra_str+" --dec "+dec_shift_r+" "+ms
              print("CMD >>> "+command)
              os.system(command)
              k+=1
          
          #ROTATION USING CASA FIXVIS
          #dec_shift="-30d43m17s"
          #k = 0
          #for file_name in file_names:
          #    options={}
          #    options["vis"]=file_name
          #    options["outputvis"]=file_name[:-3]+"F.ms"
          #    fix_vis_str = str(int(ra_h[k])) + "h" + str(int(ra_m[k])) + "m" 
          #    options["phasecenter"]='J2000 '+fix_vis_str+' '+dec_shift
          #    self.fixvis_wrapper(options) 
          #    k+=1

          os.chdir(it.PATH_CODE)

          command = "python redpipe.py --create_images F --convert_to_fits F" 
          
          
          #DIRTY IMAGE
          print("CMD >>> "+command)
          os.system(command)

          #DECONVOLVE
          print("CMD >>> "+command)
          os.system(command)
          
          os.chdir(it.PATH_DATA)

          
          k = 0
          for file_name in file_names:
              new_file_name = file_name[:-3]+"F.fits" 
              s_obj = s.stripe()
              s_obj.create_gauss_beam_fits(input_image=new_file_name,produce_beam=True,produce_beam_sqr=True,apply_beam=True,mask="F",l = rad2deg(l[k]), m = rad2deg(m[k]))
              k += 1 

          #print "diff = ",(ra_m[1]-ra_m[0])/60.0*15
          
          
          for k in xrange(len(minutes_m_vec)):
              ra_deg = (hours_m_vec[k] + minutes_m_vec[k]/60.0)*15
              list_val = self.find_fits_files_at_ra(ra_deg=ra_deg) 
              self.add_and_weigh(list_val,hours_m_vec[k],minutes_m_vec[k])
              #print str(hours_m_vec[k])+"h"+str(minutes_m_vec[k])+"m"
              #print "listval = ",list_val  
          
          os.chdir(it.PATH_CODE)
          

      def add_and_weigh(self,file_names,ra_h,ra_m):
          ra_h = int(ra_h)
          ra_m = int(ra_m)
          direc = plutil.FIGURE_PATH+"IMAGES/"
          if os.path.isdir(direc):
             os.chdir(direc)
             first = True
             if len(file_names) > 0:
                for file_name in file_names:
                    if first:
                       command = "cp "+file_name+" "+str(ra_h)+"_"+str(ra_m)+"_S.fits"  
                       print("CMD >>> "+command)
                       os.system(command) 
                       command = "cp "+file_name+" "+str(ra_h)+"_"+str(ra_m)+"_I.fits"  
                       print("CMD >>> "+command)
                       os.system(command)   
                       command = "cp "+file_name+" "+str(ra_h)+"_"+str(ra_m)+"_W.fits"  
                       print("CMD >>> "+command)
                       os.system(command)

                       fh = pyfits.open(file_name)
                       image = fh[0].data
                       image_S = image[0,0,:,:]
                       image_S[:,:] = 0
                       image_I = np.copy(image_S)
                       image_W = np.copy(image_S)       
                       fh.close()
                       first = False
                     
                    file_split = file_name.split(".")
                    beam_file = file_split[0]+"."+file_split[1]+"."+file_split[2]+"."+file_split[3]+"."+file_split[4]+".FsB.fits"                             
                    fh = pyfits.open(file_name)
                    image = fh[0].data
                    image = image[0,0,:,:]
                    fh.close()

                    image_S = image_S + image

                    fh = pyfits.open(beam_file)
                    image = fh[0].data
                    image = image[0,0,:,:]
                    fh.close()

                    print "file_name = ",file_name
                    image_W = image_W + image

                fh = pyfits.open(str(ra_h)+"_"+str(ra_m)+"_S.fits")
                fh[0].data[0,0,:,:] = image_S
                fh.writeto(str(ra_h)+"_"+str(ra_m)+"_S.fits",clobber=True)
                fh.close()

                fh = pyfits.open(str(ra_h)+"_"+str(ra_m)+"_W.fits")
                fh[0].data[0,0,:,:] = image_W
                fh.writeto(str(ra_h)+"_"+str(ra_m)+"_W.fits",clobber=True)
                fh.close()	

                image_I[image_W>0.1] = image_S[image_W>0.1]/image_W[image_W>0.1]
                image_I[image_W<0.1] = np.NaN
                #image_I = image_S/image_W 

                fh = pyfits.open(str(ra_h)+"_"+str(ra_m)+"_I.fits")
                fh[0].data[0,0,:,:] = image_I
                fh.writeto(str(ra_h)+"_"+str(ra_m)+"_I.fits",clobber=True)
                fh.close() 
          os.chdir(it.PATH_CODE)   

      def find_fits_files_at_ra(self,ra_deg,search_string="*CFB.fits"):
          direc = plutil.FIGURE_PATH+"IMAGES/"
          fits_list = np.array([])
          if os.path.isdir(direc):
             os.chdir(direc)
             file_names = glob.glob(search_string)
             for fits_file in file_names:
                 ff = pyfits.open(fits_file)
                 header_v = ff[0].header
                 ra_0 = header_v["crval1"]#degrees
                 dec_0 = header_v["crval2"]#degrees
                 ff.close()

                 if np.absolute(ra_deg - ra_0) < 1:
                     fits_list = np.append(fits_list,np.array([fits_file]))
          os.chdir(it.PATH_CODE)
          return fits_list       
                
      def create_dictionary_lm(self,min_spacing=60,search_string="*C.ms",dec_shift="-30d43m17s"):
          
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
          
          negative = False
          if dec_shift[0] == "-":
             negative = True
             dec_shift = dec_shift[1:]
 
          dec_split = dec_shift.split("d")
          d_str = dec_split[0]
          dec_split = dec_split[1].split("m")
          m_str = dec_split[0]
          s_str = dec_split[1]
          s_str = s_str[:-1]
           
          if negative:
             dec_shift = -1*deg2rad(float(d_str)+float(m_str)/60 + float(s_str)/3600) 
          else:
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
               

          print "ra_cen = ",ra_cen
          print "dec_cen = ",dec_cen * 180./np.pi
          print "dec_shift = ",dec_shift * 180./np.pi
          print "ra_shift = ",ra_shift
          print "ra_h = ",ra_h
          print "ra_m = ",ra_m  
          print "h = ",h
          print "l = ",l * 180./np.pi
          print "m = ",m * 180./np.pi
              
          os.chdir(it.PATH_CODE)
          return file_names,ra_h,ra_m,l,m,hours_m_vec,minutes_m_vec

      def create_ph_center_hour_vec(self,min_spacing=40):
          print "min_spacing = ",min_spacing
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

          print "hm = ",hours_m_vec
          print "mm = ",minutes_m_vec
          print "h = ",hours_vec
          print "m = ",minutes_vec
          print "h_r = ",h
          print "hm_r = ",hm
          return hours_m_vec,minutes_m_vec,hours_vec,minutes_vec,h,hm

              
              

if __name__ == "__main__":
   img = imager()

   img.fix_vis_beam_creator() 

   #img.create_dictionary_lm()

   #img.create_ph_center_hour_vec(16)   
