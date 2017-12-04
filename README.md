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

## Plotting utilities

`plotutilities.py` provides some basic plotting functionality:

1. Plotting autocorrelations
2. Plotting redindant groups (per baseline or combined)
3. Plotting HEX-19 with antenna labels (either ids or names)

`python plotutilities.py -a -r -l --per_baseline <value> --ymax <value> --id_true <value>`

`-a: plot all the autocorrelations for all the measurement sets in current directory`

`-r: plot all the correlations associated with the different baseline groups for all the measurement sets in current directory`

`-l: plot the HERA-19 layout with antenna labels`

`--ymax <value>: (must be a real number) On the correlation plots this is the chosen maximum y-value. Default is 6.`

`--per_baseline <value>: (must be a boolean) Produce per-baseline correlation plots. Default is False.`

`--id_true <value>: (must be a boolean) On the HERA-19 layout plot use CASA antenna names or HERA wiki ids. Default is False.`

**REMEMBER TO SET THE LOCATION OF WHERE THE FIGURES SHOULD BE STORED IN THE HEADER OF PLOTUTILITIES.PY**

## Reduction pipeline

`redpipe.py` provides some basic reduction related processing commands:

1. Manual basic flagging: antenna, baselines and auto
2. Run aoflagger (zen.2457545.48707.xx_strategy.rfis)
3. Bandpass calibration of galactic center ms
4. Transfer of bandpass solution in 2 to all ms in directory
5. Plotting of badpass cal solution in 2
6. Imaging of all ms in directory

`python redpipe.py --flag_all_basic --bandpass_gc --plot_cal_gc --apply_cal_gc_all --create_images --print_lst`

`--flag_all_basic: flag known bad channels, autocorrelations and antenna`

`--flag_ao: flag with ao flagger using strategy zen.2457545.48707.xx_strategy.rfis`

`--bandpass_gc: do a bandpass calibration on the snapshot where the galactic center is at zenith`

`--plot_cal_gc: plot the calibration bandpass solution obtained from doing a bandpass cal on the ms where gc is at zenith`

`--apply_cal_gc_all: apply the bandpass solutions obtained to all the other measurement sets in the directory`

`--create_images: call clean and viewer to create some basic images`

`--print_lst: converts the file names to lst and prints them`

** REMEMBER THAT HSA7458_V000_HH.PY AND CREATE_PS.PY HAS TO BE IN YOUR DATA DIRECTORY **

## Healpix

`stripe.py` helps convert individual fits images into an all-sky healpix map

1. Create a Gaussian HERA beam at 150 MHz (\*B.fits).
2. Apply to fits images (\*UB.fits).
3. Create a squared beam (\*sB.fits).
4. Create healpix fits images for each fits image (\*H.fits).
5. Create an all sky healpix fits image using square beam weighting and individual fits images.

`python stripe.py --create_beams --call_mk_map_mod --make_all_sky_map --plot_healpix`

`--create_beams: creating different kind of beam files, a beam, a beam times sky and a beam square file`

`--call_mk_map_mod: project all fits files to individual healpix projected fits files`

`--make_all_sky_map: make an all sky healpix map from the individual healpix-fits files (use squared beam weighting)`

`--plot_healpix: plot the all sky healpix`
