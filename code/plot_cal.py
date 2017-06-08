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

ANT_ID = np.array([80,104,96,64,53,31,65,88,9,20,89,43,105,22,81,10,72,112,97])

def plot_delays():
    global ANT_ID
    ANT_ID = np.sort(ANT_ID)
    file_names = glob.glob("./CAL/d_*.cal")
    JD_list = []
    delays = np.zeros((len(file_names),len(ANT_ID)))
    k = 0
    for file_name in file_names:
        JDs_split = file_name.split('.')
        JD_list.append(JDs_split[1].strip('/CAL/d_')) #+ '.' + JDs_split[2])
        t=table(file_name)
        #print "t.colnames() = ",t.colnames()
        ANT1 = t.getcol("ANTENNA1")
        FPAR = np.array(t.getcol("FPARAM"))
        #print "FPAR[ANT_ID,0,0] = ",FPAR[ANT_ID,0,0]
        delays[k,:] = FPAR[ANT_ID,0,0]
        k = k + 1

    #print JD_list
    
    #VERY SPECIFIC CODE [PLOTS FIRST TWO JDs]
    ax = plt.subplot(111)
    x = float(ANT_ID[k])

    ind = np.arange(len(ANT_ID)) 
    width = 0.35
    
    rects1 = ax.bar(ind,delays[0,:],width=width,color='b',align='center')
    rects2 = ax.bar(ind+width,delays[1,:],width=width,color='r',align='center')

    ax.set_ylabel(r'$\tau$ [nsec]')
    ax.set_xlabel('ANTENNA ID')
    ax.set_title('Delay at different JD\'s')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(ANT_ID)
    ax.legend((rects1[0], rects2[0]), JD_list[0:2]) 

    plt.show()

def plot_bandpass():
    global ANT_ID
    ANT_ID = np.sort(ANT_ID)
    file_names = glob.glob("./CAL/b_*.cal")
    JD_list = []
    comp_gain = np.zeros((len(file_names),len(ANT_ID),1024),dtype=complex)
    chan_width = 100.0/1024.0
    k = 0
    for file_name in file_names:
        JDs_split = file_name.split('.')
        JD_list.append(JDs_split[1].strip('/CAL/b_'))
        t=table(file_name)
        #print "t.colnames() = ",t.colnames()  
        CPAR = np.array(t.getcol("CPARAM"))
        if k == 0:
           channel = np.arange(CPAR.shape[1])
        CPAR = CPAR[ANT_ID,:,0]
        comp_gain[k,:,:] = CPAR 
        k = k + 1

    comp_gain[(np.absolute(comp_gain) < 1.001) & (np.absolute(comp_gain) > 0.999)] = np.NaN
    
    color = ['b','g'] #DAYS  
    line = ['-','--','-.'] #ANTENNAS

    for k in xrange(len(color)):
        for j in xrange(len(line)):
            plt.plot(channel,np.absolute(comp_gain[k,j,:]),color[k]+line[j],label=JD_list[k]+" - ANT:"+str(ANT_ID[j]))
             
    
    plt.xlabel("CHANNEL")
    plt.ylabel("AMP")
    plt.xlim([200,900])
    plt.title("BANDPASS: AMP")
    
    plt.legend()
    plt.show()

    color = ['b','g'] #DAYS  
    line = ['-','--','-.'] #ANTENNAS

    for k in xrange(len(color)):
        for j in xrange(len(line)):
            plt.plot(channel,np.angle(comp_gain[k,j,:],deg=True),color[k]+line[j],label=JD_list[k]+" - ANT:"+str(ANT_ID[j]))
             
    
    plt.xlabel("CHANNEL")
    plt.ylabel("PHASE")
    plt.xlim([200,900])
    plt.title("BANDPASS: PHASE")
    
    plt.legend()
    plt.show()
   

if __name__ == "__main__":
   plot_delays()
   plot_bandpass()
   

 

