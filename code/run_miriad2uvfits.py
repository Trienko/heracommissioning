import inittasks as it
import pyuvdata
import glob, os

#USING RIDHIMA's SCRIPT INSTEAD OF THE OFFICIAL PYUVDATA SCRIPT
def miriad_to_uvfits():
    os.chdir(it.PATH_DATA) 
    file_names = glob.glob("*.uvcU")
    for file_name in file_names:
        command = "python " + it.PATH_TO_MIR_TO_FITS_RID + " --nophs --uvfits --pyuvdata " + file_name
        print("CMD >>> "+command)
        os.system(command) 
        command = "mv "+file_name+"M"+".uvfits "+file_name+".uvfits"
        print("CMD >>> "+command)
        os.system(command) 
    os.chdir(it.PATH_CODE)

if __name__ == "__main__":
   miriad_to_uvfits()
