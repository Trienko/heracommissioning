from pyrap.tables import table
import inittasks as it
import os,sys
import glob
import numpy as np
import pylab as plt
import time
import matplotlib as mpl
import pickle
import dill
from concurrent import futures
import multiprocessing
#from numba import jit


class redundant_stefcal(object):
      
      def __init__(self):
          pass

      ######################################
      #Generates the antenna positions for a hexagonal grid
      ######################################
      def hex_grid(self,hex_dim,l):
          hex_dim = int(hex_dim)
          side = int(hex_dim + 1)
          ant_main_row = int(side + hex_dim)
        
          elements = 1

          #SUMMING ANTENNAS IN HEXAGONAL RINGS 
          for k in xrange(hex_dim):
              elements = elements + (k+1)*6
          
          #CREATING HEXAGONAL LAYOUT STARTING FROM CENTER      
          ant_x = np.zeros((elements,),dtype=float)
          ant_y = np.zeros((elements,),dtype=float)
          
          x = 0.0
          y = 0.0

          counter = 0
        
          for k in xrange(side):
              x_row = x
              y_row = y
              for i in xrange(ant_main_row):
                  if k == 0:
                     ant_x[counter] = x_row 
                     ant_y[counter] = y_row
                     x_row = x_row + l
                     counter = counter + 1 
                  else:
                     ant_x[counter] = x_row
                     ant_y[counter] = y_row
                     counter = counter + 1
                   
                     ant_x[counter] = x_row
                     ant_y[counter] = -1*y_row
                     x_row = x_row + l
                     counter = counter + 1   
              x = x + l/2.0
              y = y + (np.sqrt(3)/2.0)*l                 
              ant_main_row = ant_main_row - 1
       
          #RESORTING ANTENNA INDICES SO THAT LOWER LEFT CORNER BECOMES THE FIRST ANTENNA
          y_idx = np.argsort(ant_y)
          ant_y = ant_y[y_idx]
          ant_x = ant_x[y_idx]

          slice_value = int(side)
          start_index = 0
          add = True
          ant_main_row = int(side + hex_dim)

          for k in xrange(ant_main_row):
              temp_vec_x = ant_x[start_index:start_index+slice_value]
              x_idx = np.argsort(temp_vec_x)
              temp_vec_x = temp_vec_x[x_idx]
              ant_x[start_index:start_index+slice_value] = temp_vec_x
              if slice_value == ant_main_row:
                 add = False
              start_index = start_index+slice_value 
            
              if add:
                 slice_value = slice_value + 1
              else:
                 slice_value = slice_value - 1  

          #SHIFTING CENTER OF ARRAY TO ORIGIN
          max_x = np.amax(ant_x)
                    
          ant_x = ant_x - max_x/2.0
          
          temp_ant = np.zeros((len(ant_x),3),dtype=float)
          temp_ant[:,0] = ant_x
          temp_ant[:,1] = ant_y
          return temp_ant

      ######################################
      #Converts the antenna idices pq into a redundant index
      #   
      #INPUTS:
      #red_vec_x - the current list of unique redundant baseline vector (x-coordinate)
      #red_vec_y - the current list of unique redundant baseline vector (y-coordinate)
      #ant_x_p - the x coordinate of antenna p
      #ant_x_q - the x coordinate of antenna q
      #ant_y_p - the y coordinate of antenna p
      #ant_y_q - the y coordinate of antenna q
      #
      #RETURNS:
      #red_vec_x - the current list of unique redundant baseline vector (x-coordinate)
      #red_vec_y - the current list of unique redundant baseline vector (y-coordinate)
      #l - The redundant index associated with antenna p and q
      ######################################
      def determine_phi_value(self,red_vec_x,red_vec_y,ant_x_p,ant_x_q,ant_y_p,ant_y_q):
          red_x = ant_x_q - ant_x_p
          red_y = ant_y_q - ant_y_p

          for l in xrange(len(red_vec_x)):
              if (np.allclose(red_x,red_vec_x[l]) and np.allclose(red_y,red_vec_y[l])):
                 return red_vec_x,red_vec_y,int(l+1)

          red_vec_x = np.append(red_vec_x,np.array([red_x]))
          red_vec_y = np.append(red_vec_y,np.array([red_y]))
          return red_vec_x,red_vec_y,int(len(red_vec_x)) 

      ######################################
      #Returns the mapping phi, from pq indices to redundant indices.
      #INPUTS:
      #ant_x - vector containing the x-positions of all the antennas
      #ant_y - vector containing the y-positions of all the antennas 
      #
      #RETURNS:
      #phi - the mapping from pq indices to redundant indices
      #zeta - the symmetrical counterpart
      #L - maximum number of redundant groups  
      ######################################
      def calculate_phi(self,ant_x,ant_y):
          phi = np.zeros((len(ant_x),len(ant_y)),dtype=int)
          zeta = np.zeros((len(ant_x),len(ant_y)),dtype=int)
          red_vec_x = np.array([])
          red_vec_y = np.array([])
          for k in xrange(len(ant_x)):
              for j in xrange(k+1,len(ant_x)):
                  red_vec_x,red_vec_y,phi[k,j]  = self.determine_phi_value(red_vec_x,red_vec_y,ant_x[k],ant_x[j],ant_y[k],ant_y[j])           
                  zeta[k,j] = phi[k,j]
                  zeta[j,k] = zeta[k,j]
          L = np.amax(zeta)
          return phi,zeta,L

      def create_PQ(self,phi,L):

          PQ = {}
          for i in xrange(L):
              pq = zip(*np.where(phi == (i+1)))
              #print "pq2 = ",pq        
              PQ[str(i)]=pq
              #print "PQ = ",PQ    
          return PQ 
      
      #@jit 
      #@profile
      def convert_y_to_M(self,PQ,y,N):
    
          M = np.zeros((N,N),dtype=complex)
          for i in xrange(len(y)):
              pq = PQ[str(i)]
              #print "pq = ",pq
                          
              for k in xrange(len(pq)):
                  p = pq[k][0]
                  q = pq[k][1]
             
                  M[p,q] = y[i]
                  #M[q,p] = y[i].real + y[i].imag*(-1j) 
                  M[q,p] = np.conjugate(y[i]) 
          #from IPython import embed; embed() 
          return M  

      def convert_y_to_M_vec(self,A1,A2,P,y,N):
          M = np.zeros((N,N),dtype=complex)

          for i in xrange(len(y)):
              idx = (P==i)
              idxA1 = A1[idx] 
              idxA2 = A2[idx] 
              y_c = np.conjugate(y[i])
              M[idxA1,idxA2]=y[i]
              M[idxA2,idxA1]=y_c

          return M

      def construct_flag_y(self,PQ,F):
          L = len(PQ.keys())
          y = np.zeros((L,),dtype=int)    

          for i in xrange(L):
              pq = PQ[str(i)]
              #print "pq = ",pq
              temp_len = len(pq)            
              for k in xrange(len(pq)):
                  p = pq[k][0]
                  q = pq[k][1]
                  y[i] = y[i] + F[p,q]             
                     
          #from IPython import embed; embed() 
          y[y>0] = 1
          return y  

      def construct_flag_g(self,F):
          g = np.zeros((F.shape[0],),dtype=int)
          for k in xrange(len(g)):
              row = F[k,:]
              g[k]= np.sum(row)
          g[g>0] = 1
          return g

      def convert_M_to_y(self,PQ,M):
          L = len(PQ.keys())
          y = np.zeros((L,),dtype=complex)    

          for i in xrange(L):
              pq = PQ[str(i)]
              #print "pq = ",pq
              temp_len = len(pq)            
              for k in xrange(len(pq)):
                  p = pq[k][0]
                  q = pq[k][1]
                  y[i] = y[i] + M[p,q]             
              y[i] = y[i]/temp_len
          #from IPython import embed; embed() 
          return y


      def construct_A_and_P(self,phi):
          N = phi.shape[0]
          B = (N**2 - N)/2 #ASSUMING THE FILE CONTAINS AUTO-CORRELATIONS
          
          A1 = np.zeros((B,),dtype=int)
          A2 = np.zeros((B,),dtype=int)
          P = np.zeros((B,),dtype=int)
          
          counter = 0
          for k in xrange(N):
              for j in xrange(k+1,N):
                  A1[counter] = k
                  A2[counter] = j
                  P[counter] = phi[k,j]-1
                  counter = counter + 1

          idx_sort = np.argsort(P)

          P = P[idx_sort]
          A1 = A1[idx_sort]
          A2 = A2[idx_sort]

          print "P = ",P

          L = np.amax(phi)

          print "L = ",L
          print "L2 = ",np.amax(phi)

          red_sum_idx  = np.array([0]) 

          num_red = 0
          for k in xrange(L):
              num_red_temp = len(A1[P==k])
              num_red = num_red + num_red_temp
              red_sum_idx = np.append(red_sum_idx,np.array([num_red]))
              print "k = ",num_red
          
          print "red_sum_idx = ",red_sum_idx
          red_sum_idx = red_sum_idx[:-1]

          print "np.reduceat = ",np.add.reduceat(P,red_sum_idx)

          return A1,A2,P      


      def convert_M_to_y_flag(self,PQ,M,F):
          L = len(PQ.keys())
          y = np.zeros((L,),dtype=complex)
          f = np.zeros((L,),dtype=int)    

          for i in xrange(L):
              pq = PQ[str(i)]
              #print "pq = ",pq
              for k in xrange(len(pq)):
                  p = pq[k][0]
                  q = pq[k][1]
                  y[i] = y[i] + M[p,q] 
                  f[i] = f[i] + F[p,q]
            
              if f[i] == 0:
                 y[i] = 0
              else:
                 y[i] = y[i]/f[i]
          #from IPython import embed; embed() 
          return y

      #@profile
      #@jit
      def redundant_StEFCal(self,D,phi,tau=1e-3,alpha=0.3,max_itr=10,PQ=None,F=None,A1=None,A2=None,P=None):
          sum_f = np.sum(F)
          if sum_f == 0:
             #print "HALLO"
             return None,False,None,None,None,None,None,None 

          converged = False
          N = D.shape[0]
          D = np.copy(D)
          D = D - D*np.eye(N)
          
          if F is not None:
             D = F*D
             

          L = np.amax(phi)
          temp =np.ones((D.shape[0],D.shape[1]) ,dtype=complex)
    
          error_vector = np.array([])

          if A1 is None:
             #EXTRACT BASELINE INDICES FOR EACH REDUNDANT SPACING
             if PQ is None:
                PQ = self.create_PQ(phi,L)

          g_temp = np.ones((N,),dtype=complex)
          #y_temp = np.ones((L,),dtype=complex)
          if F is not None:
             y_temp = self.convert_M_to_y_flag(PQ,D,F)
             g_flag = self.construct_flag_g(F)
             g_temp = g_temp*g_flag
             y_flag = self.construct_flag_y(PQ,F)
             y_temp = y_temp*y_flag
          else:
             y_temp = self.convert_M_to_y(PQ,D)

          z_temp = np.hstack([g_temp,y_temp])

          start = time.time() 
    
          for i in xrange(max_itr): #MAX NUMBER OF ITRS
              g_old = np.copy(g_temp)
              y_old = np.copy(y_temp)
              z_old = np.copy(z_temp)
 
              if A1 is not None:
                 M = self.convert_y_to_M_vec(A1,A2,P,y_old,N) #CONVERT y VECTOR TO M matrix
              else:
                 M = self.convert_y_to_M(PQ,y_old,N) #CONVERT y VECTOR TO M matrix
              
              if F is not None:
                 M = F*M
              
              #plt.imshow(np.absolute(M))
              #plt.show()
              #from IPython import embed; embed()        
        
              for p in xrange(N): #STEFCAL - update antenna gains
                  if F is not None:
                     if g_flag[p] <> 0:
                        z = g_old*M[:,p]
                        g_temp[p] = np.sum(np.conj(D[:,p])*z)/(np.sum(np.conj(z)*z))                  
                  else:
                     z = g_old*M[:,p]
                     g_temp[p] = np.sum(np.conj(D[:,p])*z)/(np.sum(np.conj(z)*z))
        
              g_old_c = np.conjugate(g_old)

              for l in xrange(L): #UPDATE y
                  if F is not None:
                     
                     if y_flag[l] <> 0:
                        if A1 is None:
                           pq = PQ[str(l)]
                           num = 0
                           den = 0
                           for k in xrange(len(pq)): #loop through all baselines for each redundant spacing
                               p = pq[k][0]
                               q = pq[k][1]

                               num = num + np.conjugate(g_old[p])*g_old[q]*D[p,q]
                               den = den + np.absolute(g_old[p])**2*np.absolute(g_old[q])**2
                           if np.absolute(den) < 1e-6:
                              y_temp[l] = 0
                           else:
                              y_temp[l] = num/den
                        else:
                           #print "HALLO DARKNESS MY OLD FRIEND"
                           idx = (P==l)
                           idxA1 = A1[idx] 
                           idxA2 = A2[idx]
                           gA1 = g_old[idxA1]
                           gA1c = g_old_c[idxA1]
                           gA2 = g_old[idxA2]

                           num = np.sum(gA1c*gA2*D[idxA1,idxA2])
                           den = np.sum(np.absolute(gA1)**2*np.absolute(g_old[idxA2])**2)
                           if np.absolute(den) < 1e-6:
                              y_temp[l] = 0
                           else:
                              y_temp[l] = num/den 
                           #y_c = np.conjugate(y[i])
                           #M[idxA1,idxA2]=y[i]
                           #M[idxA2,idxA1]=y_c
                  else:
                     pq = PQ[str(l)]
                     num = 0
                     den = 0
                     for k in xrange(len(pq)): #loop through all baselines for each redundant spacing
                         p = pq[k][0]
                         q = pq[k][1]

                         num = num + np.conjugate(g_old[p])*g_old[q]*D[p,q]
                         den = den + np.absolute(g_old[p])**2*np.absolute(g_old[q])**2
                     if np.absolute(den) < 1e-6:
                        y_temp[l] = 0
                     else:
                        y_temp[l] = num/den
         
              g_temp = alpha*g_temp + (1-alpha)*g_old
              y_temp = alpha*y_temp + (1-alpha)*y_old
              z_temp = np.hstack([g_temp,y_temp]) #final update
              #print "g_temp =",g_temp
              #print "y_temp =",y_temp        

              #e = np.sqrt(np.sum(np.absolute(z_temp-z_old)**2))/np.sqrt(np.sum(np.absolute(z_temp)**2))
              #print "e = ",e

              err = np.sqrt(np.sum(np.absolute(z_temp-z_old)**2))/np.sqrt(np.sum(np.absolute(z_temp)**2))

              error_vector = np.append(error_vector,np.array([err]))

              if (err <= tau):
                 converged = True 
                 break

          #print "i = ",i
          #print "norm = ",np.sqrt(np.sum(np.absolute(z_temp-z_old)**2))/np.sqrt(np.sum(np.absolute(z_temp)**2))
          stop = time.time()
          G = np.dot(np.diag(g_temp),temp)
          G = np.dot(G,np.diag(g_temp.conj()))  
          M = self.convert_y_to_M(PQ,y_temp,N)         

          return z_temp,converged,G,M,start,stop,i,error_vector

      def find_indices(self,a,b):
          if a < b:
             return a,b,False
          else:
             return b,a,True

      def compute_D_cal(self,pickle_name):
           
          input = open(pickle_name, 'rb')

          #Pickle dictionary using protocol 0.
          data_mat = dill.load(input)
          G_mat = dill.load(input)
          flag_mat = dill.load(input)
          phi = dill.load(input)
          indx_2d = dill.load(input)
          PQ = dill.load(input) 

          F = np.absolute(flag_mat-1)

          G_mat[F == 0] = 1

          #D_cal = G_mat**(-1)*data_mat
     
          D_cal = np.zeros(G_mat.shape,dtype=complex)

          for f in xrange(G_mat.shape[3]):
              D_cal[:,:,:,f] = G_mat[:,:,:,f]**(-1)*data_mat[:,:,:,f] 

          return D_cal,indx_2d

      def write_to_D(self,ms_file,data_cube,indx_2d):
          t=table(ms_file,readonly=False)
          data = t.getcol("CORRECTED_DATA")
          for k in xrange(data_cube.shape[0]):
              for j in xrange(data_cube.shape[1]):
                  p,q,greater = self.find_indices(it.ANT_ID[k],it.ANT_ID[j])
                  if greater:
   		     data[indx_2d[k,j,:],:] = np.reshape(np.conjugate(data_cube[k,j,:,:]),data[indx_2d[k,j,:],:].shape)
                  else:
                     data[indx_2d[k,j,:],:] = np.reshape(data_cube[k,j,:,:],data[indx_2d[k,j,:],:].shape)

          t.putcol("CORRECTED_DATA",data)
          t.flush()
          t.close()        


      def read_in_D(self,ms_file):
          os.chdir(it.PATH_DATA)
          N = len(it.ANT_ID)
          B = (N**2 + N)/2 #ASSUMING THE FILE CONTAINS AUTO-CORRELATIONS

          t=table(ms_file)
          data = t.getcol("CORRECTED_DATA")
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
                  p,q,greater = self.find_indices(it.ANT_ID[k],it.ANT_ID[j])
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

          os.chdir(it.PATH_CODE)
          return data_mat,flag_mat,flag_row_mat,indx_2d

      def plot_a_specific_ts(self,ts,D,F,PQ):

          D_new = np.squeeze(D[:,:,ts,:])
          F_new = np.squeeze(F[:,:,ts,:])
   
          y = convert_M_to_y_flag(PQ,D_new,F)

      def apply_redundant_stefcal_multi(self,ms_file):
          os.chdir(it.PATH_DATA)
          data_mat,flag_mat,flag_row_mat, indx_2d = self.read_in_D(ms_file)
          G_mat = np.ones(data_mat.shape,dtype=complex)
          M_mat = np.ones(data_mat.shape,dtype=complex)
          ant = self.hex_grid(hex_dim=2,l=14.6)
          phi,zeta,L = self.calculate_phi(ant[:,0],ant[:,1])
          #plt.imshow(phi)
          #plt.show()
          PQ = self.create_PQ(phi,L)
          start_b = time.time()
          with futures.ProcessPoolExecutor(max_workers=4) as executor:
               for t in xrange(1):#data_mat.shape[2]
              	    F_time = np.absolute(flag_row_mat[:,:,t]-1)
                    sum_time = np.sum(F_time)
                    if sum_time <> 0:
                      #TODO:: NEED TO SHIFT FLAGGING INTO THE FUNCTION
                      future_to_f = dict((executor.submit(self.redundant_StEFCal, D=data_mat[:,:,t,f],phi=phi,tau=1e-9,alpha=1.0/3.0,max_itr=1000,PQ=PQ,F=np.absolute(flag_mat[:,:,t,f]-1)), f)
                         for f in xrange(data_mat.shape[3]))
                      counter = 0
                      for future in futures.as_completed(future_to_f):
                          counter = counter + 1
                          
                          f = future_to_f[future]
                          print "***************"
                          print "t = ",t
                          print "f = ",f
                          print "counter = ",counter
                           
                          z_temp,converged,G_temp,M_temp,start,stop,i,error_vector = future.result()
                          print "converged = ",converged
                          print "***************"
                          if converged:
                             F = np.absolute(flag_mat[:,:,t,f]-1)
                             G_temp[F==0] = 1
                             G_mat[:,:,t,f] = G_temp
                             data_temp = data_mat[:,:,t,f]
                             M_temp[F==0] = data_temp[F==0]
                             M_mat[:,:,t,f] = M_temp
                             #TODO:: STILL NEED TO DO SOMETHING IF FLAGGED IN CHANNEL
                          else:
                             G_mat[:,:,t,f] = np.ones((G_mat.shape[0],G_mat.shape[1]),dtype=complex)
                             M_mat[:,:,t,f] = data_mat[:,:,t,f]
                    else:
                       G_mat[:,:,t,:] = np.ones((G_mat.shape[0],G_mat.shape[1],1,G_mat.shape[3]),dtype=complex)
                       M_mat[:,:,t,:] = data_mat[:,:,t,:]    
          stop_b = time.time()

          print "TIME M:: ",(stop_b-start_b)
          #SOME BASIC FINAL PLOTTING

          #F = np.absolute(flag_mat[:,:,0,700]-1)
          #G_new = G_mat[:,:,0,700]
          #G_new[F==0] = np.NaN
          #plot_before_after_cal_per_t_f(data_mat[:,:,0,700],G_new,phi)
          '''
          F = np.absolute(flag_mat-1)
          G_mat[F == 0] = 1

          #D_cal = G_mat**(-1)*data_mat
     
          D_cal = np.zeros(G_mat.shape,dtype=complex)

          for f in xrange(G_mat.shape[3]):
              D_cal[:,:,:,f] = G_mat[:,:,:,f]**(-1)*data_mat[:,:,:,f] 
          '''
          '''
          output = open('data.pkl', 'wb')

          #Pickle dictionary using protocol 0.
          dill.dump(data_mat, output)
          dill.dump(G_mat, output)
          dill.dump(flag_mat,output)
          dill.dump(phi,output)
          dill.dump(indx_2d,output)
          dill.dump(PQ,output)
          
          output.close()
          '''                        
          '''
          plt.imshow(np.absolute(flag_row_mat[:,:,25]-1))
          print np.absolute(flag_row_mat[:,:,25]-1)
          print phi
          plt.show()
          plt.imshow(flag_mat[:,:,25,700])
          plt.show()
          y_flag = self.construct_flag_y(PQ,np.absolute(flag_mat[:,:,25,700]-1))
          g_flag = self.construct_flag_g(np.absolute(flag_mat[:,:,25,700]-1))
          print "y_flag = ",y_flag
          print "g_flag = ",g_flag
          print flag_mat[:,:,25,700].shape
          F = np.absolute(flag_mat[:,:,25,701]-1)
          one_array = np.ones(flag_mat[:,:,25,700].shape,dtype=int)
          y_flag = self.construct_flag_y(PQ,one_array)
          print "y_flag = ",y_flag
          plt.imshow(np.absolute(data_mat[:,:,25,701]-data_mat[:,:,25,701]*np.eye(19)))
          plt.show()
          z_temp,converged,G,M,start,stop,i,error_vector = self.redundant_StEFCal(D=data_mat[:,:,25,700],phi=phi,tau=1e-9,alpha=1.0/3.0,max_itr=1000,PQ=PQ,F=None)
          plt.imshow(np.absolute(G))
          plt.show()
          print "converged = ",converged
          plt.imshow(np.absolute(M))
          plt.show()
          plt.imshow(np.absolute(data_mat[:,:,25,700]*G**(-1)-data_mat[:,:,25,701]*np.eye(19)*G**(-1)))
          plt.show()

          G_new = np.copy(G)
          G_new[F==0] = 1

          print "G_new = ",G_new
          '''
          os.chdir(it.PATH_CODE)    
          return D_cal,indx_2d      

      def apply_redundant_stefcal(self,ms_file):
          os.chdir(it.PATH_DATA)
          data_mat,flag_mat,flag_row_mat, indx_2d = self.read_in_D(ms_file)
          G_mat = np.ones(data_mat.shape,dtype=complex)
          M_mat = np.ones(data_mat.shape,dtype=complex)
          ant = self.hex_grid(hex_dim=2,l=14.6)
          phi,zeta,L = self.calculate_phi(ant[:,0],ant[:,1])
          A1,A2,P = self.construct_A_and_P(phi)
          
          #A1 = None
          #A2 = None
          #P = None
          #plt.imshow(phi)
          #plt.show()
          PQ = self.create_PQ(phi,L)
          
          start_b = time.time()
          for t in xrange(1):#data_mat.shape[2]
              F_time = np.absolute(flag_row_mat[:,:,t]-1)
              sum_time = np.sum(F_time)
              print "t = ",t
              if sum_time <> 0:
                 for f in xrange(data_mat.shape[3]):
                     F = np.absolute(flag_mat[:,:,t,f]-1)#FLAGGING STILLL NOT CORRECT NEED TO INCORPORATE TIME FLAGS
                     sum_f = np.sum(F)
                     if sum_f <> 0:
                        #print "************************"
                        #print "t = ",t
                        print "f = ",f 
                        z_temp,converged,G_temp,M_temp,start,stop,i,error_vector = self.redundant_StEFCal(D=data_mat[:,:,t,f],phi=phi,tau=1e-9,alpha=1.0/3.0,max_itr=1000,PQ=PQ,F=F,A1=A1,A2=A2,P=P)
                        #print "converged = ",converged
                        #print "************************"
                        G_temp[F==0] = 1
                        G_mat[:,:,t,f] = G_temp
                        data_temp = data_mat[:,:,t,f]
                        M_temp[F==0] = data_temp[F==0]
                        M_mat[:,:,t,f] = M_temp
                     else:
                        G_mat[:,:,t,f] = np.ones((G_mat.shape[0],G_mat.shape[1]),dtype=complex)
                        M_mat[:,:,t,f] = data_mat[:,:,t,f]
              else:
                  G_mat[:,:,t,:] = np.ones((G_mat.shape[0],G_mat.shape[1],1,G_mat.shape[3]),dtype=complex)
                  M_mat[:,:,t,:] = data_mat[:,:,t,:] 
          stop_b = time.time() 

          print "TIME S:: (seconds)",(stop_b-start_b)

          #SOME BASIC FINAL PLOTTING

          F = np.absolute(flag_mat[:,:,0,700]-1)
          G_new = G_mat[:,:,0,700]
          G_new[F==0] = np.NaN
          plot_before_after_cal_per_t_f(data_mat[:,:,0,700],G_new,phi)
          '''
          output = open('data.pkl', 'wb')

          #Pickle dictionary using protocol 0.
          dill.dump(data_mat, output)
          dill.dump(G_mat, output)
          dill.dump(flag_mat,output)
          dill.dump(phi,output)
          dill.dump(indx_2d,output)
          dill.dump(PQ,output)
          
          output.close()
          '''                        
          '''
          plt.imshow(np.absolute(flag_row_mat[:,:,25]-1))
          print np.absolute(flag_row_mat[:,:,25]-1)
          print phi
          plt.show()
          plt.imshow(flag_mat[:,:,25,700])
          plt.show()
          y_flag = self.construct_flag_y(PQ,np.absolute(flag_mat[:,:,25,700]-1))
          g_flag = self.construct_flag_g(np.absolute(flag_mat[:,:,25,700]-1))
          print "y_flag = ",y_flag
          print "g_flag = ",g_flag
          print flag_mat[:,:,25,700].shape
          F = np.absolute(flag_mat[:,:,25,701]-1)
          one_array = np.ones(flag_mat[:,:,25,700].shape,dtype=int)
          y_flag = self.construct_flag_y(PQ,one_array)
          print "y_flag = ",y_flag
          plt.imshow(np.absolute(data_mat[:,:,25,701]-data_mat[:,:,25,701]*np.eye(19)))
          plt.show()
          z_temp,converged,G,M,start,stop,i,error_vector = self.redundant_StEFCal(D=data_mat[:,:,25,700],phi=phi,tau=1e-9,alpha=1.0/3.0,max_itr=1000,PQ=PQ,F=None)
          plt.imshow(np.absolute(G))
          plt.show()
          print "converged = ",converged
          plt.imshow(np.absolute(M))
          plt.show()
          plt.imshow(np.absolute(data_mat[:,:,25,700]*G**(-1)-data_mat[:,:,25,701]*np.eye(19)*G**(-1)))
          plt.show()

          G_new = np.copy(G)
          G_new[F==0] = 1

          print "G_new = ",G_new
          '''
          '''
          F = np.absolute(flag_mat-1)
          G_mat[F == 0] = 1

          #D_cal = G_mat**(-1)*data_mat
     
          D_cal = np.zeros(G_mat.shape,dtype=complex)

          for f in xrange(G_mat.shape[3]):
              D_cal[:,:,:,f] = G_mat[:,:,:,f]**(-1)*data_mat[:,:,:,f] 

          os.chdir(it.PATH_CODE)
          return D_cal,indx_2d 
          '''

def find_color_marker(index_value):
    color = np.array(['b','g','r','c','m','y','k'])
    marker = np.array(['o','v','^','<','>','8','s','p','*','H','+','x','D'])
    index_value = index_value-1
    counter = 0
    c_final = None
    m_final = None
    for k in xrange(len(marker)):
        for l in xrange(len(color)):
            if counter == index_value:
               c_final = color[l]
               m_final = marker[k]
               break
            counter = counter+1
        else:
            continue  # executed if the loop ended normally (no break)
        break  # executed if loop ended through break
    #print "c_final = ",c_final
    #print "m_final = ",m_final

    if c_final is None:
       i_c = np.random.randint(low=0,high=len(color))
       i_m = np.random.randint(low=0,high=len(marker)) 
       c_final = color[i_c]
       m_final = color[i_m]
    return c_final,m_final 

def plot_before_after_cal_per_t_f(D,G,phi):
        mpl.rcParams['xtick.labelsize'] = 20 
        mpl.rcParams['ytick.labelsize'] = 20 
        #mpl.rcParams['ylabel.labelsize'] = 22  
        #mpl.rcParams['xlabel.labelsize'] = 22 
        #mpl.rcParams['title.labelsize'] = 22
        D_new = D[:,:]
        G_new = G[:,:]
        D_cal = D_new*G_new**(-1)
        print "D_cal = ",D_cal
        for i in xrange(D_new.shape[0]):
            for j in xrange(i+1,D_new.shape[1]):
                ind = phi[i,j]
                #print "ind = ",ind
                c_final,m_final = find_color_marker(ind)
                plt.plot(D_new[i,j].real,D_new[i,j].imag,c_final+m_final,ms=10)
        plt.axis("equal")
        plt.xlabel("real",fontsize=15)
        plt.ylabel("imag",fontsize=15)
        plt.title("Before Calibration",fontsize=15)
        plt.show()        

        for i in xrange(D_cal.shape[0]):
            for j in xrange(i+1,D_cal.shape[1]):
                ind = phi[i,j]
                c_final,m_final = find_color_marker(ind)
                plt.plot(D_cal[i,j].real,D_cal[i,j].imag,c_final+m_final,ms=10)
        plt.axis("equal")
        plt.ylabel("imag",fontsize=15)
        plt.xlabel("real",fontsize=15)
        plt.title("After Calibration",fontsize=15)
        plt.show()

def investigate_G(pickle_name,ts=25):
    input = open(pickle_name, 'rb')

    #Pickle dictionary using protocol 0.
    data_mat = dill.load(input)
    G_mat = dill.load(input)
    flag_mat = dill.load(input)
    phi = dill.load(input)
    indx_2d = dill.load(input)
    PQ = dill.load(input)
   
    F = np.absolute(flag_mat-1)

    G_mat[F == 0] = 1

    #D_cal = G_mat**(-1)*data_mat
     
    D_cal = np.zeros(G_mat.shape,dtype=complex)

    for f in xrange(G_mat.shape[3]):
        D_cal[:,:,:,f] = G_mat[:,:,:,f]**(-1)*data_mat[:,:,:,f]

    input.close()

    print G_mat.shape

    G_mat[F==0] = np.NaN

    plot_before_after_cal_per_t_f(data_mat[:,:,ts,700],G_mat[:,:,ts,700],phi)

    result = np.zeros((len(PQ.keys()),D_cal.shape[3]),dtype=complex)

    for f in xrange(D_cal.shape[3]):
        for l in xrange(len(PQ.keys())):
            pq = PQ[str(l)]
            total = 0
            avg_total = 0
            for k in xrange(len(pq)): #loop through all baselines for each redundant spacing
                p = pq[k][0]
                q = pq[k][1]

                if not(np.isnan(G_mat[p,q,ts,f])):
                   total = total + G_mat[p,q,ts,f] 
                   avg_total = avg_total + 1 
            if avg_total <> 0:
               result[l,f] = total/avg_total
            

    #for l in xrange(len(PQ.keys())):
    #    plt.plot(np.absolute(result[l,:]))
    #plt.plot(np.absolute(result[0,:]))
    #plt.plot(result[2,:].real,result[2,:].imag,"bo")
    #plt.plot(result[1,:].real,result[1,:].imag,"ro")
    #plt.show()    

    for l in xrange(len(PQ.keys())):
        c_final,m_final = find_color_marker(l+1)
        #print c_final
        #print m_final
        plt.plot(result[l,:].real,result[l,:].imag,c_final+m_final,ms=10)
    #plt.plot(np.angle(result[1,:]))
    plt.show()               
    
if __name__ == "__main__":
   
   red_cal = redundant_stefcal()

   ant = red_cal.hex_grid(hex_dim=2,l=14.6)
   phi,zeta,L = red_cal.calculate_phi(ant[:,0],ant[:,1])
   A1,A2,P = red_cal.construct_A_and_P(phi)

   #os.chdir(it.PATH_DATA)
   #file_names = glob.glob("*uvcUC.ms")
   #os.chdir(it.PATH_CODE)
   #red_cal.apply_redundant_stefcal(file_names[0])

   #print "A1 = ",A1
   #print "A2 = ",A2
   #print "P = ",P 

   '''
   ms_names = np.array(["zen.2457545.43140.xx.HH.uvcUC.ms","zen.2457545.43836.xx.HH.uvcUC.ms","zen.2457545.44532.xx.HH.uvcUC.ms","zen.2457545.45228.xx.HH.uvcUC.ms","zen.2457545.45924.xx.HH.uvcUC.ms","zen.2457545.46620.xx.HH.uvcUC.ms","zen.2457545.47315.xx.HH.uvcUC.ms","zen.2457545.48011.xx.HH.uvcUC.ms","zen.2457545.48707.xx.HH.uvcUC.ms","zen.2457545.49403.xx.HH.uvcUC.ms","zen.2457545.50099.xx.HH.uvcUC.ms","zen.2457545.50795.xx.HH.uvcUC.ms","zen.2457545.51491.xx.HH.uvcUC.ms"])

   red_cal = redundant_stefcal()
   
   #os.chdir(it.PATH_DATA)
   #file_names = glob.glob("*uvcUC.ms")
   #os.chdir(it.PATH_CODE)

   for ms_name in ms_names: 
       print "###################"
       print "ms_name = ",msname
       #red_cal.apply_redundant_stefcal_multi(file_names[0])
       D,idx = red_cal.apply_redundant_stefcal(msname)
       os.chdir(it.PATH_DATA)
       red_cal.write_to_D(msname,D,idx)
       os.chdir(it.PATH_CODE)
       print "###################"
       #investigate_G(pickle_name="data.pkl")
       #D,idx = red_cal.compute_D_cal("data.pkl")
       #red_cal.write_to_D(file_names[0],D,idx)

       #data_mat,flag_mat,flag_row_mat,indx_2d = red_cal.read_in_D(file_names[0])

       #plt.plot(data_mat[0,3,30,:])
       #plt.show()
   '''  
