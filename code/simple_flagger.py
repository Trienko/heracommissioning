from pyrap.tables import table
#import inittasks as it
import os,sys
import glob
import numpy as np
import pylab as plt
import time
import matplotlib as mpl
import pickle
#import dill
from concurrent import futures
from concurrent.futures.process import ProcessPoolExecutor
#import multiprocessing
#import numexpr as nx
import getopt
#from numba import jit
import scipy as sp
import scipy.ndimage

from scipy import signal

HERA19_ID = np.array([80,104,96,64,53,31,65,88,9,20,89,43,105,22,81,10,72,112,97])

PATH_DATA = "/home/trienko/HERA/conference/data/STEF2/"
PATH_CODE = "/home/trienko/HERA/conference/code/"

class flagger(object):
      
      def __init__(self):
          pass

      def find_indices(self,a,b):
          if a < b:
             return a,b,False
          else:
             return b,a,True

      def read_in_D(self,ms_file,column="CORRECTED_DATA",telescope="HERA19",flag_ant=np.array([])):
          os.chdir(PATH_DATA)

          if telescope == "HERA19":
             ANT_ID = HERA19_ID
          else:
             ANT_ID = PAPER128_ID
 
          N = len(ANT_ID)

          if telescope == "HERA19":
             B = ((N+len(flag_ant))**2 + (N+len(flag_ant)))/2 #ASSUMING HERA19 CONTAINS AUTO-CORRELATIONS
          else:
             B = ((N+len(flag_ant))**2 - (N+len(flag_ant)))/2 #ASSUMING PAPER128 CONTAINS NO AUTO-CORRELATIONS         

          t=table(ms_file)
          data = t.getcol(column)
          flag = t.getcol("FLAG")
          flag_row = t.getcol("FLAG_ROW")
          ant1 = t.getcol("ANTENNA1")
          ant2 = t.getcol("ANTENNA2")
          indx_1d = np.arange(data.shape[0])

          ts = data.shape[0]/B
          chans = data.shape[1]

          data_mat = np.zeros((N,N,ts,chans),dtype=complex)
          flag_mat = np.ones((N,N,ts,chans),dtype=int)
          flag_row_mat = np.ones((N,N,ts),dtype=int)
          indx_2d = np.zeros((N,N,ts),dtype=int)

          for k in xrange(N):
              for j in xrange(k+1,N): 
                  #print "******************"
                  #print "k = ",k
                  #print "j = ",j
                  p,q,greater = self.find_indices(ANT_ID[k],ANT_ID[j])
                  #print "p = ",p
                  #print "q = ",q
                  #print "******************"
                  temp_indx = np.logical_and(ant1==p,ant2==q)
                  
                  if greater:
                     data_mat[k,j,:,:] = np.conjugate(data[temp_indx,:,0])
                     data_mat[j,k,:,:] = data[temp_indx,:,0]
                  else:
                     data_mat[k,j,:,:] = data[temp_indx,:,0]
                     data_mat[j,k,:,:] = np.conjugate(data[temp_indx,:,0])

                  flag_mat[k,j,:,:] = flag[temp_indx,:,0]
                  flag_mat[j,k,:,:] = flag[temp_indx,:,0]
 
                  flag_row_mat[k,j,:] = flag_row[temp_indx]
                  flag_row_mat[j,k,:] = flag_row[temp_indx]

                  indx_2d[k,j,:] = indx_1d[temp_indx] 

          #print "data_chunck = ",data_chunck.shape
          #print data.shape
          #print flag.shape

          os.chdir(PATH_CODE)
          return data_mat,flag_mat,flag_row_mat,indx_2d

      def write_to_D(self,ms_file,data_cube,indx_2d,column="CORRECTED_DATA",telescope="HERA19"):
          os.chdir(PATH_DATA)
          
          if telescope == "HERA19":
             ANT_ID = HERA19_ID
          else:
             ANT_ID = PAPER128_ID
             
          #print "ms_file = ",ms_file
          #command = "pwd"
          #print("CMD >>> "+command)
          #os.system(command)
          
          t=table(ms_file,readonly=False)
          data = t.getcol(column)
          for k in xrange(data_cube.shape[0]):
              for j in xrange(k+1,data_cube.shape[1]):
                  p,q,greater = self.find_indices(ANT_ID[k],ANT_ID[j])
                  if column == "FLAG":
                     data[indx_2d[k,j,:],:] = np.reshape(data_cube[k,j,:,:],data[indx_2d[k,j,:],:].shape)
                  else:
                     if greater:
   		        data[indx_2d[k,j,:],:] = np.reshape(np.conjugate(data_cube[k,j,:,:]),data[indx_2d[k,j,:],:].shape)
                     else:
                        data[indx_2d[k,j,:],:] = np.reshape(data_cube[k,j,:,:],data[indx_2d[k,j,:],:].shape)

          t.putcol(column,data)
          t.flush()
          t.close()
          os.chdir(PATH_CODE) 

def flag_data(data_mat, flag_mat, med_filter_size=9, sigma_factor=0.01, agreement=30):

    new_flag_mat = np.zeros(flag_mat.shape,dtype=int)

    data_mat = np.average(data_mat,axis=2)

    a1 = np.array([],dtype=int)
    a2 = np.array([],dtype=int)

    for k in xrange(data_mat.shape[0]):
        for j in xrange(k+1,data_mat.shape[1]):
            #print "k = ",k
            #print "j = ",j
            a1 = np.append(a1,np.array([k]))
            a2 = np.append(a2,np.array([j]))

            input_signal = np.absolute(data_mat[k,j,:])
            f_signal = sp.signal.medfilt(input_signal,med_filter_size)
                       
            #abs_error = 100*(np.square(f_signal-input_signal)/np.square(f_signal))

            a_error = np.absolute(f_signal - input_signal)

            #median = np.median(a_error)

            #mad = np.median(np.absolute(a_error-median))

            std = np.std(a_error) 

            #print "mean = ", np.mean(s_error)
            #print "std = ",np.std(a_error) 

            #print "median = ",median
            #print "mad = ",mad
         
            chan = np.arange(len(input_signal))
            flag_values = chan[a_error>sigma_factor*std]
            #print "flag_values = ",flag_values
            new_flag_mat[k,j,:,flag_values] = 1

            input_signal[flag_values]=np.NaN
            #plt.plot(input_signal)

    #plt.show()

    B = len(new_flag_mat[a1,a2,0,0])

    for k in xrange(new_flag_mat.shape[3]):
        sub_flag = new_flag_mat[a1,a2,0,k]

        value = np.sum(sub_flag)

        P = 100*((1.0*value)/B)

        #print "k = ",k
        #print "P = ",P

        if P > agreement:
           new_flag_mat[:,:,:,k] = 1

    '''
    for k in xrange(data_mat.shape[0]):
        for j in xrange(k+1,data_mat.shape[1]):
            input_signal = np.absolute(data_mat[k,j,:])

            flag_values = new_flag_mat[k,j,0,:]
            #print "flag_value2 = ",flag_values

            input_signal[flag_values==1]=np.NaN
            plt.plot(input_signal)

    plt.show()
    '''	     		
    #flag_mat[new_flag_mat==1] = 1

    flag_mat = new_flag_mat
    
    return flag_mat    

if __name__ == "__main__":
   
   f = flagger()
   data_mat,flag_mat,flag_row_mat,indx_2d = f.read_in_D(ms_file="zen.2457661.16694.xx.HH.uvcU.ms",column="DATA",telescope="HERA19",flag_ant=np.array([]))
   flag_mat = flag_data(data_mat, flag_mat, med_filter_size=9, sigma_factor=0.02, agreement=30)

   f.write_to_D(ms_file="zen.2457661.16694.xx.HH.uvcU.ms",data_cube=flag_mat,indx_2d=indx_2d, column="FLAG", telescope="HERA19")

   #print flag_mat[0,1,0,0].type   
   '''
   data_avg_in_time = np.average(data_mat,axis=2)

   signal = data_avg_in_time[0,1,:]
   
   #plt.plot(np.absolute(data_avg_in_time[0,1,:]))

   print data_avg_in_time[0,1,:].shape
     
   f_output = sp.signal.medfilt(np.absolute(data_avg_in_time[0,1,:]),9)

   abs_error = 100*np.absolute((np.absolute(f_output)-np.absolute(data_avg_in_time[0,1,:])))**2/(np.absolute(f_output[:]))**2

   chan = np.arange(data_avg_in_time.shape[2])

   signal[abs_error>0.005] = np.NaN

   #plt.plot(np.absolute(f_output),"r")
   plt.plot(np.absolute(signal),"b")
   
   plt.show() 

   #plt.plot(np.absolute(data_avg_in_time[0,1,:]),"b")

   #plt.plot(np.absolute(f_output),"r")

   #plt.show(100*np.absolute((np.absolute(f_output)-np.absolute(data_avg_in_time[0,1,:])))**2/(np.absolute(f_output[:]))**2)

   #plt.plot()
   

   #plt.plot(np.absolute((np.absolute(f_output)-np.absolute(data_avg_in_time[0,1,:])))**2,"r")
   #plt.show()

   #plt.plot(100*np.absolute((np.absolute(f_output[200:800])-np.absolute(data_avg_in_time[0,1,200:800])))**2/(np.absolute(f_output[200:800]))**2,"r")
   #plt.show()
   
   #print data_mat.shape

   #print data_avg_in_time.shape
   '''   
   '''
   t = np.linspace(0,10,200) # create a time signal
   x1 = np.sin(t) # create a simple sine wave
   x2 = x1 + 7*np.random.rand(200) # add noise to the signal
   y1 = sp.signal.medfilt(x2,21) # add noise to the signal
   # plot the results
   plt.subplot(2,1,1)
   plt.plot(t,x2,'yo-')
   plt.title('input wave')
   plt.xlabel('time')
   plt.subplot(2,1,2)
   plt.plot(range(200),y1,'yo-')
   plt.title('filtered wave')
   plt.xlabel('time')
   plt.show()
   '''
   

    

