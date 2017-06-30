import inittasks as it
import pyuvdata
import glob, os

def uv_fits_to_miriad():
    os.chdir(it.PATH_DATA)
    for file_name in glob.glob("*C.uvfits"):
        from pyuvdata import UVData
        miriad_file = file_name[:-7]
        UV = UVData()
        UV.read_uvfits(file_name,run_check=False,run_check_acceptability=False)
        UV.write_miriad(miriad_file,run_check=False,run_check_acceptability=False,clobber=True)
    os.chdir(it.PATH_CODE)

if __name__ == "__main__":
   uv_fits_to_miriad()
