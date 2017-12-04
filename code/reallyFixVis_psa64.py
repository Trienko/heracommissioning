#!/usr/bin/env python
"""
Apply a 'correct' phase correction to MS
"""

import numpy as np
import sys,os
import ClassMS_psa64

if __name__ == '__main__':
    from optparse import OptionParser
    o = OptionParser()
    o.set_usage('%prog [options] --ra [RA] --dec [DEC] MS_FILES')
    o.set_description(__doc__)
    o.add_option('-r', '--ra', dest='ra', default=None,
        help='RA (in radians unless flag set) to phase data to')
    o.add_option('-d', '--dec', dest='dec', default=None,
        help='DEC (in radians unless flag set) to phase data to')
    o.add_option('--deg',dest='deg_flag',action='store_true',
        help='Use degrees in stead of radians')
    o.add_option('--str',dest='str_flag', action='store_true',
        help='Use hh:mm:ss.sss format for RA and dd:mm:ss.sss format for DEC')
    o.add_option('--col',dest='colName', default='CORRECTED_DATA',
        help='Select which data column to write visibilites to, default: CORRECTED_DATA')
    opts, args = o.parse_args(sys.argv[1:])

    if opts.ra is None or opts.dec is None:
        print 'ERROR: RA or DEC not set'
        exit(1)

    if opts.deg_flag:
        ra=np.pi*float(opts.ra)/180.
        dec=np.pi*float(opts.dec)/180.
    elif opts.str_flag:
        raArr=map(float,opts.ra.split(':'))
        ra=15.*(raArr[0]+raArr[1]/60.+raArr[2]/3600.)
        ra=np.pi*ra/180.
        decArr=map(float,opts.dec.split(':'))
        dec=np.abs(decArr[0])+decArr[1]/60.+decArr[2]/3600.
        if decArr[0] < 0.: dec*=-1.
        dec=np.pi*dec/180.
    else:
        ra=float(opts.ra)
        dec=float(opts.dec)

    print 'Phasing to RA: %1.10f, DEC: %1.10f'%(ra,dec)

    nfiles=len(args)
    for fid,fn in enumerate(args):
        print 'Applying phase correction to (%i of %i):'%(fid,nfiles),fn
        MS=ClassMS_psa64.ClassMS(fn,Col="CORRECTED_DATA")
        MS.RotateMS((ra,dec))
        MS.SaveVis(Col=opts.colName)
    print 'Completed'
