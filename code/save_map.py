#!/usr/bin/env python
"""
Save a HEALPIX FITS map
"""

import sys,os
import numpy as n
import healpy as h

if __name__ == '__main__':
    from optparse import OptionParser
    o = OptionParser()
    o.set_usage('%prog [options] FITS_MAPS')
    o.set_description(__doc__)
    o.add_option('-s','--save',dest='savemap',default=None,help='Save map to file')
    #o.add_option(tion(__doc__)
    opts, args = o.parse_args(sys.argv[1:])

    m=None
    w=None
    for fits in args:
        print 'Opening:',fits
        fitssplt = fits.split('/')[-1].split('.')
        JD = fitssplt[0] + '.' + fitssplt[1]
        #POL = 'xx'
        #beam = '%s.%s.B_healpix.fits'%(JD,POL)
        path,srcFits=os.path.split(os.path.realpath(fits))
        #destBm = os.path.join(path,beam)
        if m is None: 
            m,w,hdr=h.read_map(fits,field=(0,1),h=True)
            #bm,bw,bhdr=h.read_map(destBm,field=(0,1),h=True)
        else:
            m0,w0,hdr=h.read_map(fits,field=(0,1),h=True)
            #bm0,bw0,bhdr=h.read_map(destBm,field=(0,1),h=True)
            m+=m0
            w+=w0
            #bm+=bm0
    if not(opts.savemap is None):
        ofn=opts.savemap
        #h.write_map(ofn,n.array([m/bm,w,w]),dtype=n.float64,coord='E')
        h.write_map(ofn,n.array([m,w,w]),dtype=n.float64,coord='E')

