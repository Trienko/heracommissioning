import os

if __name__ == "__main__":

   command = "python initscript.py --add_uvws --sudo_miriad_to_uvfits --importuvfits --swap_ant"
   print("CMD >>> "+command)
   os.system(command)  

   command = "python redpipe.py -d --flag_all_basic --bandpass_gc --plot_cal_gc --apply_cal_gc_all --create_images U --convert_to_fits U"
   print("CMD >>> "+command)
   os.system(command)  

   command = "python stripe.py --create_beams U"
   print("CMD >>> "+command)
   os.system(command)

   command = "python absolute_flux.py --abs_cal"
   print("CMD >>> "+command)
   os.system(command) 

   command = "python redpipe.py --create_images C --convert_to_fits C"
   print("CMD >>> "+command)
   os.system(command) 

   command = "python redpipe.py --decon_mask --create_images C --convert_to_fits C"
   print("CMD >>> "+command)
   os.system(command)

   command = "python stripe.py --create_beams C --call_mk_map_mod --make_all_sky_map --plot_healpix"
   print("CMD >>> "+command)
   os.system(command)  
 
