# Some basic scripts for HERA commissioning

## Initialization Tasks

Two python files working in unison:

1. `inittasks.py` - contains the class that performs all the initialization tasks
2. `initscript.py` - wrapper around inittasks.py, provides command line interface (applies tasks to all files in data direcotry)

`python initscript.py -h`

`python initscript.py -h --add_uvws --miriad_to_uvfits --sudo_miriad_to_uvfits --add_HERA --importuvfits --swap_ant --del_uvfits --del_uvcU --del_ms`

`--add_uvws: adds uv-tracks to miriad data sets`

`--miriad_to_uvfits: converts miriad data sets to uvfits format`

`--sudo_miriad_to_uvfits: converts miriad data sets to uvfits format (as root)`

`--add_HERA: adds HERA to CASA's observatory table (only once)`

`--importuvfits: converts uvfits to ms`

`--swap_ant: swaps the antenna columns s.t. A1 < A2`

`--del_uvfits: deletes uvfits files`

`--del_uvcU: deletes uvcU files`

`--del_ms: deletes ms files`

**REMEMBER TO SET THE LOCATIONS TO ALL THE IMPORTANT SCRIPTS AND DATA FILES IN THE HEADER OF INITTASKS.PY**


