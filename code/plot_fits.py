import aplpy
import pylab as plt
import os,glob
import numpy as np
import matplotlib.image as mgimg
import matplotlib.animation as animation
#from animate import *
#ffmpeg -framerate 1 -i image%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
from matplotlib import rcParams

#2017-10-03 09:48:48 INFO listobs	  0         zenith              18:00:23.837624 -30.43.18.87239 J2000   0          10640
#2017-10-03 09:49:46 INFO listobs	  0         zenith              05:24:10.303668 -30.44.09.29414 J2000   0          10640
#2017-10-03 09:50:09 INFO listobs	  0         zenith              21:01:20.744398 -30.47.16.72729 J2000   0          10640

#-30d43m17s

DEC = np.array([-30-43.0/60-23.837624/3600,-30-44.0/60-9.29414/3600,-30-47.0/60-16.72729/3600,-30-43.0/60-17.0/3600,-30-43.0/60-17.0/3600,-30-43.0/60-17.0/3600])
RA = np.array([18+0.0/60+23.837624/3600,5+24.0/60+10.303668/3600,21+1.0/60+20.744398/3600,5+15.0/60,18+15.0/60,21+15/60])
RA = RA*15

W1 = "5_15_I.fits"
W2 = "18_15_I.fits"
W3 = "21_15_I.fits" 

GC_FILE = "zen.2457545.47315.xx.HH.uvcUC.fits"
GC_FILE2 = "zen.2457545.47315.xx.HH.uvcU.fits"
GC_FILE3 = "zen.2457545.47315.xx.HH.uvcU_raw.fits"

FILE1 = "zen.2457661.16694.xx.HH.uvcUCF.fits"
FILE2 = "zen.2457661.64018.xx.HH.uvcUCF.fits"
FILE3 = "zen.2457661.29221.xx.HH.uvcUCF.fits"


#GC_FILE2 = "zen.2457555.44531.xx.HH.uvcU.fits"
ABS_FILE = "zen.2457555.57754.xx.HH.uvcUC.fits"
#IMAGE_PATH = "/home/trienko/HERA/conference/data/2457545/figures/IMAGES"
#SEARCH_STRING = "*uvcUC.fits"

def make_video():
    os.chdir(IMAGE_PATH)     
    file_names = glob.glob(SEARCH_STRING)
    JD = np.zeros((len(file_names),),dtype=float)
    JD2 = np.copy(JD)
    #beam_names =  
    
    k = 0
    for file_name in file_names:
        file_strip = file_name.split(".")
        JD[k] = float(file_strip[1]+"."+file_strip[2])
        JD2[k] = float(file_strip[2])
        k = k + 1

    srt_idx = np.argsort(JD)

    file_names = np.array(file_names)

    file_names = file_names[srt_idx]
    JD = JD[srt_idx]
    JD2 = JD2[srt_idx]

    k = 0
    for file_name in file_names:
        gc = aplpy.FITSFigure(file_name)
        file_strip = file_name.split(".")
        beam_name = file_strip[0]+"."+file_strip[1]+"."+file_strip[2]+"."+file_strip[3]+"."+file_strip[4]+".B.fits"
        gc.show_colorscale(cmap="cubehelix_r",vmin=0,vmax=40)#vmax, vmin
        gc.show_contour(beam_name,colors="blue",alpha=0.5,linewidths=0.8,linestyles="dashed")
        gc.add_grid()
        gc.grid.set_color('black') 
        gc.grid.set_alpha(0.5)
        gc.add_colorbar()
        gc.colorbar.set_axis_label_text('Jy/beam')
        gc.set_title(str(JD[k]))
        if np.absolute(JD2[k] - 47315) <= 2089:
           gc.show_circles([266.417],[-29.00781],[3],color="r")
           gc.add_label(266.417,-29.00781+5, 'Sgr A', color="r",size=12)
        if np.absolute(JD2[k] - 60538) <= 1393:
           gc.show_circles([315.32625],[-28.031944],[1.5],color="k")
           gc.show_circles([316.8554167],[-25.02777777777778],[1.5],color="k")
           gc.add_label(315.32625,-28.031944-2.2, 'PMN J2101 2802 (~27.79 Jy @ 150MHz)', color="k",size=12)
           gc.add_label(316.8554167,-25.02777777777778+2.2, 'PMN J2107 2526 (~57.39 Jy @ 150MHz)', color="k",size=12)
        plt.tight_layout()
        if k < 10:
           plt.savefig("image00"+str(k)+".png")
        else:
           plt.savefig("image0"+str(k)+".png")
        k = k+1
        gc.close()
    
    '''
    fig = plt.figure()
    
    # initiate an empty  list of "plotted" images 
    myimages = []

    #loops through available png:s
    for p in xrange(len(file_names)):

        ## Read in picture
        fname = "image"+str(p)+".png" 
        img = mgimg.imread(fname)
        imgplot = plt.imshow(img)

        # append AxesImage object to the list
        myimages.append([imgplot])

    ## create an instance of animation
    my_anim = animation.ArtistAnimation(fig, myimages, interval=1000, blit=True, repeat_delay=1000)

    ## NB: The 'save' method here belongs to the object you created above
    #my_anim.save("animation.mp4")

    ## Showtime!
    plt.show()
    '''

def plot_fits(fits_file):
    gc = aplpy.FITSFigure(fits_file)
    gc.show_colorscale(cmap="cubehelix_r",vmin=0)#vmax, vmin
    gc.add_grid()
    gc.grid.set_color('black') 
    gc.grid.set_alpha(0.5)
    gc.add_colorbar()
    gc.show_circles([266.417],[-29.00781],[2],color="r")
    gc.add_label(266.417,-29.00781+3, 'Sgr A', color="r",size=18)
    gc.axis_labels.set_font(size=20)
    gc.tick_labels.set_font(size=20) 
    gc.grid.set_xspacing(25)
    gc.ticks.set_xspacing(25)
    gc.colorbar.set_axis_label_text('Jy/beam')
    gc.colorbar.set_font(size=20)
    gc.colorbar.set_axis_label_font(size=20)
    #gc.set_title("Galactic Centre")
    plt.tight_layout()
    #rcParams.update({'figure.autolayout': True})
    plt.savefig("GC.png",bbox_inches='tight')
    plt.show()

def plot_fits_gianni(fits_file,k=0):
    gc = aplpy.FITSFigure(fits_file)
    gc.show_colorscale(cmap="jet",vmin=0,pmin=0,pmax=100)#vmax, vmin
    if k <> -1:
       gc.recenter(RA[k],DEC[k],radius=8)
    gc.add_grid()
    gc.grid.set_color('black') 
    gc.grid.set_alpha(0.5)
    gc.add_colorbar()
    gc.axis_labels.set_font(size=16)
    gc.tick_labels.set_font(size=16) 
    gc.grid.set_xspacing(5)
    gc.ticks.set_xspacing(10)
    gc.colorbar.set_axis_label_text('Jy/beam')
    gc.colorbar.set_font(size=16)
    gc.colorbar.set_axis_label_font(size=16)
    #gc.set_title("Galactic Centre")
    plt.tight_layout()
    #rcParams.update({'figure.autolayout': True})
    plt.savefig(fits_file[:-5]+".png",bbox_inches='tight')
    plt.show()

def plot_fits2(fits_file):
    gc = aplpy.FITSFigure(fits_file)
    gc.show_colorscale(cmap="cubehelix_r",vmin=0)#vmax, vmin
    gc.show_circles([315.32625],[-28.031944],[1.5],color="k")
    gc.show_circles([316.8554167],[-25.02777777777778],[1.5],color="k")
    gc.add_label(315.32625,-28.031944-2.2, 'PMN J2101 2802 (~27.79 Jy @ 150MHz)', color="k",size=18)
    gc.add_label(316.8554167,-25.02777777777778+2.2, 'PMN J2107 2526 (~57.39 Jy @ 150MHz)', color="k",size=18)
    gc.add_grid()
    gc.axis_labels.set_font(size=20)
    gc.tick_labels.set_font(size=20) 
    gc.grid.set_xspacing(25)
    gc.ticks.set_xspacing(25)
    gc.grid.set_color('black') 
    gc.grid.set_alpha(0.5)
    
    gc.add_colorbar()
    gc.colorbar.set_axis_label_text('Jy/beam')
    gc.colorbar.set_font(size=20)
    gc.colorbar.set_axis_label_font(size=20)
    #gc.set_title("Absolute Flux Calibrators")
    plt.tight_layout()
    #rcParams.update({'figure.autolayout': True})
    plt.savefig("ABS.png",bbox_inches='tight')
    plt.show()

def plot_psf(fits_file="psf.fits"):
    gc = aplpy.FITSFigure(fits_file)
    gc.show_colorscale(cmap="cubehelix_r",pmin=0,pmax=100)#vmax, vmin
    gc.add_grid()
    gc.grid.set_color('black') 
    gc.grid.set_alpha(0.5)
    gc.add_colorbar()
    #gc.colorbar.set_axis_label_text('Jy/beam')
    gc.set_title("PSF")
    plt.tight_layout()
    plt.savefig("PSF.png")
    plt.show()


if __name__=="__main__":


   print "DEC = ",DEC
   print "RA = ",RA
   plot_fits_gianni(fits_file=FILE1,k=0)
   plot_fits_gianni(fits_file=FILE2,k=1)
   plot_fits_gianni(fits_file=FILE3,k=2)

 
   plot_fits_gianni(fits_file=W1,k=3)
   plot_fits_gianni(fits_file=W2,k=4)
   plot_fits_gianni(fits_file=W3,k=5)
   
   #plot_psf()
   #plot_fits(fits_file=GC_FILE)
   #plot_fits(fits_file=GC_FILE3)
   #plot_fits2(fits_file=ABS_FILE)
   #make_video() 
    
    
