import inittasks as it
#import pyuvdata
import glob, os
#import redpipe as red
#import absolute_flux as absf

if __name__ == "__main__":

   #TESTING TRANSFER OF GAINS ACCROSS JD'S
   #***********************************************************************************
   #command = "python redpipe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/ --apply_cal_gc_spec"
   #print("CMD >>> "+command)
   #os.system(command)

   #INITIALIZATION
   #***********************************************************************************
   command = "python initscript.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/ --add_uvws --sudo_miriad_to_uvfits --importuvfits"
   print("CMD >>> "+command)
   os.system(command)

   command = "python initscript.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457555/ --add_uvws --sudo_miriad_to_uvfits --importuvfits"
   print("CMD >>> "+command)
   os.system(command)

   command = "python initscript.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/ --add_uvws --sudo_miriad_to_uvfits --importuvfits"
   print("CMD >>> "+command)
   os.system(command)

   command = "python initscript.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457748/ --add_uvws --sudo miriad_to_uvfits --importuvfits"
   print("CMD >>> "+command)
   os.system(command)


   #CALIBRATING FIRST MS
   #***********************************************************************************
   #it.PATH_DATA = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/"

   #command = "python initscript.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/ --add_uvws --sudo_miriad_to_uvfits --importuvfits --swap_ant"
   #print("CMD >>> "+command)
   #os.system(command)

   #command = "python redpipe.py -d --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/"
   #print("CMD >>> "+command)
   #os.system(command)
   
   command = "python redpipe.py -d --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/ --flag_all_basic --bandpass_gc --apply_cal_gc_all --plot_cal_gc --create_images U --convert_to_fits U"
   print("CMD >>> "+command)
   os.system(command)

   command = "python stripe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/ --create_beams U"
   print("CMD >>> "+command)
   os.system(command)

   command = "python absolute_flux.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/ --abs_cal"
   print("CMD >>> "+command)
   os.system(command)

   command = "python redpipe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457545/ --create_images C --convert_to_fits C"
   print("CMD >>> "+command)
   os.system(command)

   #CALIBRATING SECOND MS
   #***********************************************************************************
   #it.PATH_DATA = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457555/"

   command = "python redpipe.py -d --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457555/ --flag_all_basic --bandpass_gc --apply_cal_gc_all --plot_cal_gc --create_images U --convert_to_fits U"
   print("CMD >>> "+command)
   os.system(command)

   command = "python stripe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457555/ --create_beams U"
   print("CMD >>> "+command)
   os.system(command)

   command = "python absolute_flux.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457555/ --abs_cal"
   print("CMD >>> "+command)
   os.system(command)

   command = "python redpipe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457555/ --create_images C --convert_to_fits C"
   print("CMD >>> "+command)
   os.system(command)

   #CALIBRATING THIRD MS
   #***********************************************************************************
   #it.PATH_DATA = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/"

   command = "python redpipe.py -d --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/ --flag_all_basic --bandpass_gc --apply_cal_gc_all --plot_cal_gc --create_images U --convert_to_fits U"
   print("CMD >>> "+command)
   os.system(command)

   command = "python stripe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/ --create_beams U"
   print("CMD >>> "+command)
   os.system(command)

   command = "python absolute_flux.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/ --abs_cal"
   print("CMD >>> "+command)
   os.system(command)

   command = "python redpipe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/ --create_images C --convert_to_fits C"
   print("CMD >>> "+command)
   os.system(command)

   #CALIBRATING FOURTH MS
   #***********************************************************************************
   #it.PATH_DATA = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457748/"
   #it.SPEC_GC_DIR = "/media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457661/"

   command = "python redpipe.py -d --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457748/ --flag_all_basic --apply_cal_gc_spec --create_images U --convert_to_fits U"
   print("CMD >>> "+command)
   os.system(command)

   #command = "python stripe.py --create_beams U"
   #print("CMD >>> "+command)
   #os.system(command)

   command = "python absolute_flux.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457748/ --apply_spec"
   print("CMD >>> "+command)
   os.system(command)

   command = "python redpipe.py --set_data_path /media/tlgrobler/0514a1d6-e58b-451b-8187-92d24de8df69/data/2457748/ --create_images C --convert_to_fits C"
   print("CMD >>> "+command)
   os.system(command)
   '''
   #command = "python redpipe.py --create_images C --convert_to_fits C"
   #print("CMD >>> "+command)
   #os.system(command)
  
   #inittasks_object = it.inittasks()
   #red_object = red.redpipe()
   #abs_object = absf.absflux()

   #inittasks_object.split_sim_ms(ms_file="simvis-noiseless.ms",dummy_ms="dummy.ms",column="DATA")
   #inittasks_object.create_t0_pickle()
   #inittasks_object.compute_t0_str()
   #inittasks_object.rename_rephase_split_ms()

   #inittasks_object.create_time_pickle_N()
   #inittasks_object.compute_time_str_N()
   #inittasks_object.split_and_unphase_ms_N()
   
   #inittasks_object.compute_time_str()
   #inittasks_object.split_and_unphase_ms()
   
   '''
   inittasks_object.add_uv_tracks()
   #inittasks_object.miriad_to_uvfits_rid()
   
   command = "python initscript.py --sudo_miriad_to_uvfits"
   print("CMD >>> "+command)
   os.system(command)
      
   inittasks_object.remove_ms()
   inittasks_object.uv_fits_to_ms()
   inittasks_object.swap_antenna()
   #inittasks_object.apply_flags()

   command = "python redpipe.py -d --flag_all_basic --bandpass_gc --apply_cal_gc_all"
   print("CMD >>> "+command)
   os.system(command)
   
   #red_object.applycal_gc_all(delay=True)
   abs_object.apply_c()
   inittasks_object.ms_to_uv_fits()
   inittasks_object.uvfits_to_miriad()

#for filename in args:
#    UV = pyuvdata.UVData()
#    UV.read_miriad(filename, 'miriad')
#    outfilename = filename + '.uvfits'
#    UV.phase_to_time(UV.time_array[0])
#    UV.write_uvfits(outfilename, 'uvfits')
#show()

#if opts.opt=='pyuvdata':
#   from pyuvdata import UVData
#   print 'Using pyuvdata for conversion'
#   print 'Converting %s to %s'%(uvfits, miriad_file)
#   UV = UVData()
#   UV.read_uvfits(uvfits,run_check=False,run_check_acceptability=False)
#   UV.write_miriad(miriad_file,run_check=False, run_check_acceptability=False,clobber=True)
    '''
