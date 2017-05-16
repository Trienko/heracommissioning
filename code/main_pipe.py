python initscript.py -h --add_uvws --miriad_to_uvfits --sudo_miriad_to_uvfits --importuvfits --swap_ant

python redpipe.py --flag_all_basic --bandpass_gc --plotcal_gc --applycal_gc_all --create_images

python stripe.py --create_beams U

python absolute_flux.py --abs_cal

python stripe.py --create_beams C --call_mk_map_mod --make_all_sky_map --plot_healpix



 
