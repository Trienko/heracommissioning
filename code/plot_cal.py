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
import matplotlib

#MSNAME: zen.2457555.44531.xx.HH.uvcU.ms, UTC: 2016/6/15 22:41:15 (LST 17:45:30.84 = 4.649182)
#MSNAME: zen.2457545.47315.xx.HH.uvcU.ms, UTC: 2016/6/5 23:21:20 (LST 17:46:17.25 = 4.652557)
#MSNAME: zen.2457661.16694.xx.HH.uvcU.ms, UTC: 2016/9/29 16:00:24 (LST 18:01:28.59 = 4.718831)

ANT_ID = np.array([80,104,96,64,53,31,65,88,9,20,89,43,105,22,81,10,72,112,97])

def plot_delays():
    global ANT_ID
    matplotlib.rcParams.update({'font.size': 22})
    ANT_ID = np.sort(ANT_ID)
    file_names = glob.glob("./CAL/d_*.cal")
    JD_list = []
    JD_list_num = []
    delays = np.zeros((len(file_names),len(ANT_ID)))
    k = 0
    for file_name in file_names:
        JDs_split = file_name.split('.')
        JD_list.append(JDs_split[1].strip('/CAL/d_')) #+ '.' + JDs_split[2])
        JD_list_num.append(int(JDs_split[1].strip('/CAL/d_')))
        t=table(file_name)
        #print "t.colnames() = ",t.colnames()
        ANT1 = t.getcol("ANTENNA1")
        FPAR = np.array(t.getcol("FPARAM"))
        #print "FPAR[ANT_ID,0,0] = ",FPAR[ANT_ID,0,0]
        delays[k,:] = FPAR[ANT_ID,0,0]
        k = k + 1
    
    #print np.absolute(delays[0,:]-delays[1,:])
    #print delays[0,:]
    #print delays[1,:]
    #print np.sqrt(np.sum(np.absolute(delays[0,:]-delays[1,:])**2)/len(ANT_ID))
    #print np.sqrt(np.sum(np.absolute(delays[0,:]-delays[2,:])**2)/len(ANT_ID))

    JD_list = np.array(JD_list)

    idx = np.argsort(JD_list_num)

    JD_list = JD_list[idx]
    delays = delays[idx,:]
    delays[0,3]=0
    print delays[0,:]
    print delays[1,:]
    print np.absolute(delays[0,:]-delays[1,:])**2
    print np.sqrt(np.sum(np.absolute(delays[0,:]-delays[1,:])**2)/len(ANT_ID))
    #print np.sqrt(np.sum(np.absolute(delays[0,:]-delays[2,:])**2)/len(ANT_ID))
    #print JD_list
    
    #VERY SPECIFIC CODE [PLOTS FIRST TWO JDs]
    ax = plt.subplot(111)
    x = float(ANT_ID[k])

    ind = np.arange(len(ANT_ID[ANT_ID<=72])) 
    width = 0.3
    
    rects1 = ax.bar(ind,delays[0,ANT_ID<=72],width=width,color='b',align='center')
    rects2 = ax.bar(ind+width,delays[1,ANT_ID<=72],width=width,color='r',align='center')
    rects3 = ax.bar(ind+2*width,delays[2,ANT_ID<=72],width=width,color='g',align='center')

    ax.set_ylabel(r'$\tau$ (ns)')
    ax.set_xlabel('ANTENNA ID')
    #ax.set_title('Delay at different JD\'s')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(ANT_ID)
    #ax.legend((rects1[0], rects2[0],rects3[0]), JD_list[0:3]) 
    
    plt.show()
    return idx

def plot_bandpass(idx):
    matplotlib.rcParams.update({'font.size': 22})
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

    freq = 100 + chan_width*(channel) + chan_width/2.0

    print "freq = ",freq

    JD_list = np.array(JD_list)
    JD_list = JD_list[idx]
    comp_gain = comp_gain[idx,:,:]

    comp_gain[(np.absolute(comp_gain) < 1.001) & (np.absolute(comp_gain) > 0.999)] = np.NaN
    comp_gain[:,:,882:887] = np.NaN
    
    color = ['b','r','g'] #DAYS  
    line = ['-','--'] #ANTENNAS

    for k in xrange(len(color)):
        for j in xrange(len(line)):
            plt.plot(freq,np.absolute(comp_gain[k,j,:]),color[k]+line[j],label="ANT:"+str(ANT_ID[j]),lw=2.0)
             
    
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("Gain amplitude")
    plt.xlim([100+chan_width*200+chan_width/2.0,100+chan_width*900+chan_width/2.0])
    #plt.title("BANDPASS: AMP")
    matplotlib.rcParams.update({'font.size': 14})
    plt.legend()
    plt.show()
    matplotlib.rcParams.update({'font.size': 22})
    color = ['b','r','g'] #DAYS  
    line = ['-','--'] #ANTENNAS

    for k in xrange(len(color)):
        for j in xrange(len(line)):
            plt.plot(freq,np.angle(comp_gain[k,j,:],deg=True),color[k]+line[j],label="ANT:"+str(ANT_ID[j]),lw=2.0)
             
    
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("Gain phase (degrees)")
    plt.xlim([100+chan_width*200+chan_width/2.0,100+chan_width*900+chan_width/2.0])
    #plt.title("BANDPASS: PHASE")
    matplotlib.rcParams.update({'font.size': 14})
    plt.legend()
    
    plt.show()
   

def plot_bandpass_2(idx):
    matplotlib.rcParams.update({'font.size': 22})
    global ANT_ID
    ANT_ID = np.sort(ANT_ID)
    file_names = glob.glob("./CAL/b_*.alone.cal")
    print file_names
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

    freq = 100 + chan_width*(channel) + chan_width/2.0

    print "freq = ",freq

    JD_list = np.array(JD_list)
    JD_list = JD_list[idx]
    comp_gain = comp_gain[idx,:,:]

    #comp_gain[(np.absolute(comp_gain) < 1.001) & (np.absolute(comp_gain) > 0.999)] = np.NaN
    comp_gain[:,:,882:887] = np.NaN
    
    

    color = ['b','r'] #DAYS  
    line = ['-','--'] #ANTENNAS

    print "ANT_ID = ",ANT_ID

    print comp_gain.shape
    
    index_v = np.array([3, 5]) 
    for k in xrange(len(color)):
        for j in xrange(len(line)):
            print "ANT = ",ANT_ID[index_v[j]]
            print "index_v[j] = ",index_v[j]

            print "c_gain = ",comp_gain[k,index_v[j],:]
            plt.plot(freq,np.absolute(comp_gain[k,index_v[j],:]),color[k]+line[j],label="ANT:"+str(ANT_ID[index_v[j]]),lw=2.0)
             
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("Gain amplitude")
    plt.xlim([100+chan_width*200+chan_width/2.0,100+chan_width*900+chan_width/2.0])
    #plt.title("BANDPASS: AMP")
    matplotlib.rcParams.update({'font.size': 14})
    plt.legend()
    plt.show()
    matplotlib.rcParams.update({'font.size': 22})
    color = ['b','r'] #DAYS  
    line = ['-','--'] #ANTENNAS

    for k in xrange(len(color)):
        for j in xrange(len(line)):
            plt.plot(freq,np.angle(comp_gain[k,index_v[j],:],deg=True),color[k]+line[j],label="ANT:"+str(ANT_ID[index_v[j]]),lw=2.0)
             
    
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("Gain phase (degrees)")
    plt.xlim([100+chan_width*200+chan_width/2.0,100+chan_width*900+chan_width/2.0])
    #plt.title("BANDPASS: PHASE")
    matplotlib.rcParams.update({'font.size': 14})
    plt.legend()
    
    plt.show()

if __name__ == "__main__":
   idx = plot_delays()
   #plot_bandpass_2(idx=[0,1])
   

 

