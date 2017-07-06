import inittasks as it
import pyuvdata
import glob, os
import redpipe as red
import absolute_flux as absf

if __name__ == "__main__":
   
   inittasks_object = it.inittasks()
   red_object = red.redpipe()
   abs_object = absf.absflux()

   inittasks_object.split_ms()
   #inittasks_object.compute_time_str()
   #inittasks_object.create_time_pickle()

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
