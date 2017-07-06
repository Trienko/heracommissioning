from ephem import *
import numpy as np
import pylab as plt
import glob, os
import inittasks as it
import plotutilities as plutil
import sys, getopt
import pyfits
import pickle
from pyrap.tables import table
import healpy as hp
import matplotlib
import healpy as hp
from pylab import cm

ANT_ID = np.array([80,104,96,64,53,31,65,88,9,20,89,43,105,22,81,10,72,112,97])

x = [ 2457311,  2457325,  2457338,  2457414,  2457416,  2457417,  2457418,
  2457419,  2457420,  2457421,  2457422,  2457423,  2457424,  2457425,
  2457426,  2457427,  2457444,  2457443,  2457447,  2457456,  2457457,
  2457458,  2457607,  2457567,  2457663,  2457675,  2457470,  2457666,
  2457471,  2457668,  2457561,  2457579,  2457722,  2457606,  2457615,
  2457571,  2457583,  2457545,  2457566,  2457546,  2457627,  2457589,
  2457716,  2457718,  2457552,  2457671,  2457608,  2457628,  2457630,
  2457625,  2457564,  2457637,  2457600,  2457618,  2457613,  2457595,
  2457599,  2457570,  2457548,  2457550,  2457581,  2457597,  2457720,
  2457721,  2457551,  2457669,  2457553,  2457612,  2457617,  2457665,
  2457715,  2457554,  2457643,  2457629,  2457569,  2457670,  2457598,
  2457560,  2457717,  2457719,  2457547,  2457673,  2457549,  2457674,
  2457616,  2457732,  2457633,  2457563,  2457676,  2457594,  2457644,
  2457605,  2457565,  2457591,  2457576,  2457558,  2457620,  2457603,
  2457672,  2457593,  2457568,  2457555,  2457661,  2457562,  2457580,
  2457602,  2457610,  2457626,  2457662,  2457592,  2457654,  2457578,
  2457642,  2457572,  2457634,  2457582,  2457624,  2457621,  2457631,
  2457585,  2457677,  2457636,  2457596,  2457655,  2457604,  2457622,
  2457733,  2457587,  2457667,  2457556,  2457609,  2457574,  2457573,
  2457664,  2457678,  2457559,  2457638,  2457734,  2457632,  2457601,
  2457619,  2457575,  2457709,  2457679,  2457557,  2457635,  2457614,
  2457611,  2457623,  2457577,  2457680,  2457745,  2457753,  2457770,
  2457792,  2457735,  2457724,  2457750,  2457788,  2457681,  2457785,
  2457729,  2457754,  2457771,  2457787,  2457683,  2457686,  2457687,
  2457689,  2457731,  2457755,  2457772,  2457791,  2457695,  2457789,
  2457704,  2457707,  2457708,  2457725,  2457751,  2457768,  2457590,
  2457763,  2457780,  2457696,  2457699,  2457703,  2457706,  2457736,
  2457756,  2457773,  2457786,  2457588,  2457705,  2457726,  2457738,
  2457742,  2457764,  2457781,  2457586,  2457692,  2457739,  2457757,
  2457774,  2457790,  2457698,  2457702,  2457713,  2457740,  2457758,
  2457775,  2457793,  2457584,  2457711,  2457727,  2457744,  2457748,
  2457765,  2457782,  2457682,  2457766,  2457783,  2457684,  2457685,
  2457690,  2457694,  2457746,  2457759,  2457776,  2457794,  2457697,
  2457701,  2457747,  2457760,  2457777,  2457795,  2457741,  2457761,
  2457778,  2457796,  2457710,  2457767,  2457784,  2457723,  2457730,
  2457752,  2457769,  2457688,  2457691,  2457693,  2457743,  2457762,
  2457779,  2457797,  2457700,  2457712,  2457714,  2457728,  2457737,
  2457749,  2457798,  2457800,  2457799]

y = [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
   0,   0,   0,   0,   0,   0,  72,   6,   6,  72,  72,   0,  72,   5,  72,
   6,   6,  72,   6,   6,   6,   6,  72,   6,  72,   6,   6,  72,  72,  72,
  72,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,  72,  72,
   6,   6,  72,  72,  72,  72,  72,   6,   6,  72,  72,  72,   6,   6,   6,
  72,   6,   6,  72,  72,  72,  72,  72,  72,   6,   6,   6,   6,  72,   6,
   6,   6,   6,   6,   6,   6,   6,   6,  72,   6,   6,  72,  72,   5,   6,
   6,   6,   6,  72,   6,  28,   6,   4,   6,   6,   6,   6,   6,   6,   6,
  72,   6,   6,  31,   6,   6,   6,   6,  72,   6,   6,   6,   6,  72,  72,
   6,   6,   6,   6,   6,   6,   6,  72,  72,   6,   6,   6,   6,   6,   6,
  72,  72,  72,  72,  72,   6,  72,  72,  72,  72,  72,   6,  72,  72,  72,
  72,  72,  72,  72,   6,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,
  72,   6,  72,  72,  72,  72,  72,  72,   6,  72,  72,  72,   6,  72,   6,
   6,  72,  72,  72,   6,  72,   6,  72,  72,  72,  72,  72,  72,   6,  72,
  72,  72,   6,  72,   6,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,
  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,  64,  59,  72,  72,  39,
  72,  72,  72,  72,   6,  72,  72,  72,  72,  72,  72,  72,  72,  72,  72,
  72,  72,   6,   6,  72,  72,   1,  39]

def plot_xy():
    plt.plot(x,y,'bo')
    plt.ticklabel_format(useOffset=False)
    plt.xlabel('JD')
    plt.ylabel('Number of files')
    plt.title('Number of files with search string *xx*HH*uvc')
    plt.show()

def plotting_file_numbers_per_JD():
    dir_names = glob.glob("2*")
    dir_numbers = np.zeros((len(dir_names),))
    dir_count = np.zeros((len(dir_names),))
    k = 0
    for dir_name in dir_names:
        if os.path.isdir(dir_name):
           dir_numbers[k] = int(dir_name)
           file_names = glob.glob("./"+dir_name+"/*xx*HH*uvc") 
           dir_count[k] = len(file_names)
           k = k + 1
    print dir_numbers
    print dir_count
    #plt.plot(dir_numbers,dir_count)
    #plt.savefig("dir_content.png")


def plot_strip_cartview():
    haslam = hp.read_map('ALL_SKY.fits')
    proj_map = hp.cartview(haslam,coord=['C'], min = -60,max=60,xsize=2000, return_projected_map=True,title="HERA19: 150MHz",cbar=False)   
    fig = plt.figure()
    ax = fig.add_subplot(111)
    matplotlib.rcParams.update({'font.size': 8})

    #replot the projected healpy map
    ax.imshow(proj_map[::-1,:],vmax=60,vmin=-60, extent=[12,-12,-90,90],aspect='auto')
    
    

    names = np.array(["Vernal Equinox","Sagitarius A","PMN J2101 2802","PMN J210 2526"])
    ra = np.array([0,(17 + 42./60 + 9./3600)-24,(21+1./60+18.3/3600)-24,(21+7./60+25.3/3600)-24])
    dec = np.array([0,-28-50./60,-28-1./50-55./3600,-25-25./3600-40./3600])

    #mark the positions of important radio sources
    ax.plot(ra,dec,'ro',ms=5,mfc="None")
    for k in xrange(len(names)):
        ax.annotate(names[k], xy = (ra[k],dec[k]), xytext=(ra[k]+0.8, dec[k]+5))

       
    #create userdefined axis labels and ticks
    ax.set_xlim(12,-12)
    ax.set_ylim(-90,90)
    ticks = np.array([-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,80,90])
    plt.yticks(ticks)
    ticks = np.array([12,10,8,6,4,2,0,-2,-4,-8,-6,-10,-12])
    plt.xticks(ticks)
    plt.xlabel("Right Ascension [$h$]")
    plt.ylabel("Declination [$^{\circ}$]")
    plt.title("Haslam 408 MHz with no filtering")

    #relabel the tick values
    fig.canvas.draw()
    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels = np.array(["12$^h$","10$^h$","8$^h$","6$^h$","4$^h$","2$^h$","0$^h$","22$^h$","20$^h$","18$^h$","16$^h$","14$^h$","12$^h$"])
    ax.set_xticklabels(labels)
    labels = [item.get_text() for item in ax.get_yticklabels()]
    labels = np.array(["-90$^{\circ}$","-80$^{\circ}$","-70$^{\circ}$","-60$^{\circ}$","-50$^{\circ}$","-40$^{\circ}$","-30$^{\circ}$","-20$^{\circ}$","-10$^{\circ}$","0$^{\circ}$","10$^{\circ}$","20$^{\circ}$","30$^{\circ}$","40$^{\circ}$","50$^{\circ}$","60$^{\circ}$","70$^{\circ}$","80$^{\circ}$","90$^{\circ}$"])
    ax.set_yticklabels(labels)
    ax.grid('on')
    #ax.set_ylim(0,-50)
    plt.show()
    
def plot_healpix(file_name="ALL_SKY.FITS",field=0,max_v=60,min_v=0):
    #file_names = glob.glob("*_healpix.fits") 
    haslam = hp.read_map(file_name,field=field)
            
    for x in xrange(len(haslam)):
          if np.allclose(haslam[x],0.0):
             haslam[x] = hp.UNSEEN 

    #print "haslam = ",haslam

    cmap=cm.jet
    cmap.set_over(cmap(1.0))
    cmap.set_under('w')
    cmap.set_bad('gray')

    proj_map = hp.mollview(haslam,coord=['C'], xsize=2000,return_projected_map=True,title='',max=max_v,min=min_v,cmap=cmap)#max=0.4
    #proj_map = hp.mollview(haslam,coord=['C'], xsize=2000,return_projected_map=True,title='',cmap=cmap)
    hp.graticule()
    f = file_name[:-5]
    plt.savefig(f+str(field)+".png")          

    plt.show()

def main(argv):
    input_file = "ALL_SKY.fits"
    field = 0
    max_v = 60
    min_v = 0

    try:
       opts, args = getopt.getopt(argv,"h", ["input_file=","field=","max_v=","min_v="])
    except getopt.GetoptError:
       print 'python plot_healpix.py --input_file <value> --field <value> --max_v <value> --min_v <value>'
       sys.exit(2)
    for opt, arg in opts:
        #print "opt = ",opt
        #print "arg = ",arg
        if opt == '-h':
           print 'python plot_healpix.py --input_file <value> --field <value> --max_v <value> --min_v <value>'
           print '--input_file <value>: The healpix fits file to plot.'
           print '--field <value>: Which field in this file to plot. (0-2).'
           print '--max_v <value>: Maximum value.'
           print '--min_v <value>: Minimum value.'
           sys.exit()
        elif opt == "--input_file":
           input_file = arg
        elif opt == "--field":
           field = int(arg)
        elif opt == "--max_v":
           max_v = float(arg)  
        elif opt == "--min_v":
           min_v = float(arg)

    plot_healpix(file_name=input_file,field=field,max_v=max_v,min_v=min_v)


if __name__ == "__main__":
   main(sys.argv[1:])
   #plot_strip_cartview()
   #plot_xy()

