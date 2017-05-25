import os

if __name__ == "__main__":

   command = "python initscript.py -h --add_uvws --miriad_to_uvfits --sudo_miriad_to_uvfits --importuvfits --swap_ant"
   print("CMD >>> "+command)
   os.system(command)  

   command = "redpipe.py --flag_all_basic --bandpass_gc --plotcal_gc --applycal_gc_all --create_images"
   print("CMD >>> "+command)
   os.system(command)  

   command = "stripe.py --create_beams U"
   print("CMD >>> "+command)
   os.system(command)

   command = "absolute_flux.py --abs_cal"
   print("CMD >>> "+command)
   os.system(command)  

   command = "python stripe.py --create_beams C --call_mk_map_mod --make_all_sky_map --plot_healpix"
   print("CMD >>> "+command)
   os.system(command)  
 
