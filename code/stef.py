from pyrap.tables import table
import inittasks as it
import os,sys
import glob
import numpy as np
import pylab as plt


class redundant_stefcal():
      
      def __init__(self):
          pass

      def find_indices(self,a,b):
          if a < b:
             return a,b
          else:
             return b,a 
 
      def read_in_D(self,ms_file):
          os.chdir(it.PATH_DATA)
          N = len(it.ANT_ID)
          B = (N**2 + N)/2 #ASSUMING THE FILE CONTAINS AUTOCORRELATIONS

          t=table(ms_file)
          data = t.getcol("DATA")
          flag = t.getcol("FLAG")
          flag_row = t.getcol("FLAG_ROW")
          ant1 = t.getcol("ANTENNA1")
          ant2 = t.getcol("ANTENNA2")
          indx_1d = np.arange(data.shape[0])

          print "indx_1d = ",indx_1d
          
          ts = data.shape[0]/B
          chans = data.shape[1]

          data_mat = np.zeros((N,N,ts,chans),dtype=complex)
          flag_mat = np.zeros((N,N,ts,chans),dtype=int)
          flag_row_mat = np.zeros((N,N,ts),dtype=int)
          indx_2d = np.zeros((N,N,ts),dtype=int)

          for k in xrange(N):
              for j in xrange(k,N):
                  p,q = self.find_indices(it.ANT_ID[k],it.ANT_ID[j])
                  temp_indx = np.logical_and(ant1==p,ant2==q)
                  data_mat[k,j,:,:] = data[temp_indx,:,0]
                  flag_mat[k,j,:,:] = flag[temp_indx,:,0]
                  flag_row_mat[k,j,:] = flag_row[temp_indx]
                  indx_2d = indx_1d[temp_indx] 

          #print "data_chunck = ",data_chunck.shape
          #print data.shape
          #print flag.shape

          os.chdir(it.PATH_CODE)
          return data_mat,flag_mat,flag_row_mat,indx_2d

if __name__ == "__main__":
   red_cal = redundant_stefcal()
   os.chdir(it.PATH_DATA)
   file_names = glob.glob("*uvcU.ms")
   os.chdir(it.PATH_CODE)
   data_mat,flag_mat,flag_row_mat, indx_2d = red_cal.read_in_D(file_names[0])

   plt.plot(data_mat[0,3,30,:])
   plt.show()

