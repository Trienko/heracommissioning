#!/usr/bin/env python
#
#
#
import sys,os
import pyfits as pf
import healpy as hp
import pylab as plt
import numpy as np
#
#
#
def correct_image(input_image,input_beam,output_image):
#
 fh = pf.open(input_image)
 image = fh[0].data
 fh.close()
#
 image[0,0,:,:] = image[0,0,:,:] / input_beam
# 
 cmd = 'cp ' + input_image + ' ' + output_image
 os.system(cmd)
 fh = pf.open(output_image)
 fh[0].data = image
 fh.writeto(output_image,clobber=True)
 fh.close()
#
#
#
def make_stokes_IQ(input_XX_image,input_YY_image,output_I_image,output_Q_image):
 fh = pf.open(input_XX_image)
 xx_image = fh[0].data
 fh.close()
#
 fh = pf.open(input_YY_image)
 yy_image = fh[0].data
 fh.close()
#
 cmd = 'cp ' + input_XX_image + ' ' + output_I_image
 os.system(cmd)
 fh = pf.open(output_I_image)
 fh[0].data = (xx_image + yy_image)/2
 fh.writeto(output_I_image,clobber=True)
 fh.close()
#
 cmd = 'cp ' + input_XX_image + ' ' + output_Q_image
 os.system(cmd)
 fh = pf.open(output_Q_image)
 fh[0].data = (xx_image - yy_image)/2
 fh.writeto(output_Q_image,clobber=True)
 fh.close()
#
#
#
def weigh_image(input_image,input_beam,output_image):
 fh = pf.open(input_beam)
 beam = fh[0].data
 fh.close()
#
 fh = pf.open(input_image)
 image = fh[0].data
 fh.close()
#
 image = image * beam
# 
 cmd = 'cp ' + input_image + ' ' + output_image
 os.system(cmd)
 fh = pf.open(output_image)
 fh[0].data = image
 fh.writeto(output_image,clobber=True)
 fh.close()
#
#
#
def make_weights(input_image,input_beam,output_image):
 fh = pf.open(input_beam)
 beam = fh[0].data
 fh.close()
# 
 cmd = 'cp ' + input_image + ' ' + output_image
 os.system(cmd)
 fh = pf.open(output_image)
 image = fh[0].data
 image[0,0,:,:] = beam * beam
 fh[0].data = image
 fh.writeto(output_image,clobber=True)
 fh.close()





#
dir_string = '/home/gianni/PAPER/psa32/data/'
filenames = ['zen.2455819.50285.uvcRRECXRM.MS','zen.2455819.50981.uvcRRECXRM.MS','zen.2455819.51677.uvcRRECXRM.MS','zen.2455819.52373.uvcRRECXRM.MS','zen.2455819.53069.uvcRRECXRM.MS','zen.2455819.53765.uvcRRECXRM.MS','zen.2455819.54461.uvcRRECXRM.MS','zen.2455819.55157.uvcRRECXRM.MS','zen.2455819.55853.uvcRRECXRM.MS','zen.2455819.56548.uvcRRECXRM.MS','zen.2455819.57244.uvcRRECXRM.MS','zen.2455819.57940.uvcRRECXRM.MS','zen.2455819.58636.uvcRRECXRM.MS','zen.2455819.59332.uvcRRECXRM.MS','zen.2455819.60028.uvcRRECXRM.MS','zen.2455819.60724.uvcRRECXRM.MS','zen.2455819.61420.uvcRRECXRM.MS','zen.2455819.62116.uvcRRECXRM.MS','zen.2455819.62812.uvcRRECXRM.MS','zen.2455819.63508.uvcRRECXRM.MS','zen.2455819.64204.uvcRRECXRM.MS','zen.2455819.64900.uvcRRECXRM.MS','zen.2455819.65596.uvcRRECXRM.MS','zen.2455819.66292.uvcRRECXRM.MS','zen.2455819.66988.uvcRRECXRM.MS','zen.2455819.67684.uvcRRECXRM.MS','zen.2455819.68380.uvcRRECXRM.MS','zen.2455819.69075.uvcRRECXRM.MS','zen.2455819.69771.uvcRRECXRM.MS']
#filenames = ['zen.2455819.50285.uvcRRECXRM.MS']
#
fekoXpol='/home/gianni/PAPER/beams/fitBeam/data/PAPER_FF_X.ffe'		# path where the beams are stored
fekoYpol='/home/gianni/PAPER/beams/fitBeam/data/PAPER_FF_Y.ffe'		# path where the beams are stored
#
poln = ['XX','XY','XYi','YY']
poln = ['XX','YY']
#
image_size = '1204'
image_scale = '0.05'
nside = '512'
image_size = '2048'
image_scale = '0.025'
nside = '1024'
#image_size = '5000'
#image_scale = '0.01'
#nside = '2048'
#
# run the CASA imager as its mfs seems to give better results than the WSclean one. Make sure that the file list is the same in the CASA script and here
#
cmd = 'casapy --nologger --log2term --nologfile -c casa_clean.py'
os.system(cmd)
#
# loop through the various snapshots
#
for i in range(0,len(filenames)):
 filename = filenames[i]
 a = filename.strip('zen.')
 lst = a.strip('.uvcRRECXRM.MS')
 out_image = 'test'
 out_image = filename.strip('.uvcRRECXRM.MS')
#
#
#
 if i == 0:
#
# compute the beam from the feko sims, pointed at zenith and regridded in the wcs image coordinates. Only do it for the first snapshot as the beam remains constant
#
  cmd = 'python /home/gianni/PAPER/psa32/Grif_pipeline/genInterpBeam_GB.py --xpol ' + fekoXpol + ' --ypol ' + fekoYpol + ' -S -o beam ' + out_image + '-XX-image.fits'
  os.system(cmd)
#
# read the XX and YY beams and use them afterwards
#
  beam = np.load('beam.npy')
  beam_xx = beam[0,0,:,:]
  beam_xx = beam_xx / np.max(beam_xx)
  beam_yy = beam[5,0,:,:]
  beam_yy = beam_yy / np.max(beam_yy)
#
# now correct the individual snapshots. There is still some stuff that needs to be cleaned up
#
 for n in range(0,len(poln)):
  correct_image(out_image + '-' + poln[n] + '-image.fits',beam_xx,out_image + '-' + poln[n] + '-divided.fits')
  correct_image(out_image + '-' + poln[n] + '-image.fits',beam_yy,out_image + '-' + poln[n] + '-divided.fits')
#  weigh_image(out_image + '-' + poln[n] + '-image.fits','jones' + poln[n] + '.fits',out_image + '-' + poln[n] + '-weighted.fits')
#  make_weights(out_image + '-' + poln[n] + '-image.fits','jones' + poln[n] + '.fits',out_image + '-' + poln[n] + '-weights.fits')
## correct_image(out_image + '-YY-image.fits','jonesYY.fits',out_image + '-YY-divided.fits')
## correct_image(out_image + '-XY-image.fits','jonesXY.fits',out_image + '-XY-divided.fits')		# note that the XY image coming out of WSclean is equal to the U image coming out of the CASA imager
## correct_image(out_image + '-XYi-image.fits','jonesXYi.fits',out_image + '-XYi-divided.fits')		# note that the XYi image coming out of WSclean is equal to the -V image coming out of the CASA imager
#  make_stokes_IQ(out_image + '-XX-divided.fits',out_image + '-YY-divided.fits',out_image + '-I-divided-cross-check.fits',out_image + '-Q-divided-cross-check.fits')
## weigh_image(out_image + '-XX-image.fits','jonesXX.fits',out_image + '-XX-weighted.fits')
## weigh_image(out_image + '-YY-image.fits','jonesYY.fits',out_image + '-YY-weighted.fits')
## weigh_image(out_image + '-XY-image.fits','jonesXY.fits',out_image + '-XY-weighted.fits')	 	# note that the XY image coming out of WSclean is equal to the U image coming out of the CASA imager
## weigh_image(out_image + '-XYi-image.fits','jonesXYi.fits',out_image + '-XYi-weighted.fits') 	     	# note that the XYi image coming out of WSclean is equal to the -V image coming out of the CASA imager
#
#
# reproject each snapshot on the Healpix sphere
#
  cmd = 'python /home/gianni/PAPER/psa32/Grif_pipeline/mk_map_mod.py ' + out_image + '-' + poln[n] + '-divided.fits -i -m ' + out_image + '_' + poln[n] + '_healpix.fits -n --nside=' + nside
  os.system(cmd)
#
# now stitch the various Healpix snapshots together
#
for n in range(0,len(poln)):
 cmd = 'python /home/gianni/PAPER/psa32/Grif_pipeline/save_map.py *' + poln[n] + '_healpix.fits -s all_sky_' + poln[n] + '.fits'
 os.system(cmd)
#
# finally convert to Stokes I & Q
#
os.system('rm all_sky_I.fits all_sky_Q.fits')
cmd = 'python /home/gianni/PAPER/psa32/Grif_pipeline/make_stokes_IQ_healpix.py all_sky_XX.fits all_sky_YY.fits -s all_sky_I.fits -q all_sky_Q.fits'
os.system(cmd)
cmd = 'python /home/gianni/PAPER/psa32/Grif_pipeline/plot_map.py all_sky_I.fits -m I -p C --cmap=Greys'
##os.system(cmd)
