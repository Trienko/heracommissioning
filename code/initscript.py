import numpy as np
import pylab as plt
import glob, os
import inittasks
import sys, getopt

def main(argv):
   inittasks_object = inittasks.inittasks()
      
   try:
      opts, args = getopt.getopt(argv,"h",["add_uvws","miriad_to_uvfits","sudo_miriad_to_uvfits","add_HERA","importuvfits","swap_ant","del_uvfits","del_uvcU","del_ms"])
   except getopt.GetoptError:
      print 'python initscript.py -h --add_uvws --miriad_to_uvfits --sudo_miriad_to_uvfits --add_HERA --importuvfits --swap_ant --del_uvfits --del_uvcU --del_ms'
      sys.exit(2)
   for opt, arg in opts:
      print "opt = ",opt
      if opt == '-h':
         print 'python initscript.py -h --add_uvws --miriad_to_uvfits --sudo_miriad_to_uvfits --add_HERA --importuvfits --swap_ant --del_uvfits --del_uvcU --del_ms'
         print "--add_uvws: adds uv-tracks to miriad data sets"
         print "--miriad_to_uvfits: converts miriad data sets to uvfits format"
         print "--sudo_miriad_to_uvfits: converts miriad data sets to uvfits format (as root)"
         print "--add_HERA: adds HERA to CASA's observatory table (only once)"
         print "--importuvfits: converts uvfits to ms"
         print "--swap_ant: swaps the antenna columns s.t. A1 < A2"
         print "--del_uvfits: deletes uvfits files"
         print "--del_uvcU: deletes uvcU files"
         print "--del_ms: deletes ms files"
         print "REMEMBER TO SET THE LOCATIONS TO ALL THE IMPORTANT SCRIPTS AND DATA FILES IN THE HEADER OF INITTASKS.PY"
         sys.exit()
      elif opt == "--add_uvws":
         inittasks_object.add_uv_tracks()
      elif opt == "--miriad_to_uvfits":
         inittasks_object.miriad_to_uvfits()
      elif opt == "--sudo_miriad_to_uvfits":
         command = "sudo ipython inittasks.py"
         print("CMD >>> "+command)
         os.system(command)
      elif opt == "--addHERA":
         inittasks_object.add_HERA_observatory()
      elif opt == "--importuvfits":
         inittasks_object.uv_fits_to_ms()
      elif opt == "--swap_ant":
         inittasks_object.swap_antenna()
      elif opt == "--del_uvfits":
         inittasks_object.remove_uvfits()
      elif opt == "--del_uvcU":
         inittasks_object.remove_uvcU()
      elif opt == "--del_ms":
         inittasks_object.remove_ms()

if __name__ == "__main__":
   main(sys.argv[1:])