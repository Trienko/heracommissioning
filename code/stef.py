from pyrap.tables import table
import inittasks as it
import os,sys
import glob
import numpy as np
import pylab as plt
import time
import matplotlib as mpl


class redundant_stefcal():
      
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

      def convert_y_to_M(self,PQ,y,N):
    
          M = np.zeros((N,N),dtype=complex)
          for i in xrange(len(y)):
              pq = PQ[str(i)]
              #print "pq = ",pq
                          
              for k in xrange(len(pq)):
                  p = pq[k][0]
                  q = pq[k][1]
             
                  M[p,q] = y[i]
                  M[q,p] = np.conjugate(y[i])  
          #from IPython import embed; embed() 
          return M  

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

      def redundant_StEFCal(self,D,phi,tau=1e-3,alpha=0.3,max_itr=10,PQ=None):
          converged = False
          N = D.shape[0]
          D = D - D*np.eye(N)
          L = np.amax(phi)
          temp =np.ones((D.shape[0],D.shape[1]) ,dtype=complex)
    
          error_vector = np.array([])

          #EXTRACT BASELINE INDICES FOR EACH REDUNDANT SPACING
          if PQ is not None:
             PQ = self.create_PQ(phi,L)

          g_temp = np.ones((N,),dtype=complex)
          #y_temp = np.ones((L,),dtype=complex)
          y_temp = self.convert_M_to_y(PQ,D)
          z_temp = np.hstack([g_temp,y_temp])


          start = time.time() 
    
          for i in xrange(max_itr): #MAX NUMBER OF ITRS
              g_old = np.copy(g_temp)
              y_old = np.copy(y_temp)
              z_old = np.copy(z_temp)
 
              M = self.convert_y_to_M(PQ,y_old,N) #CONVERT y VECTOR TO M matrix
    
              #plt.imshow(np.absolute(M))
              #plt.show()
              #from IPython import embed; embed()        
        
              for p in xrange(N): #STEFCAL - update antenna gains
                  z = g_old*M[:,p]
                  g_temp[p] = np.sum(np.conj(D[:,p])*z)/(np.sum(np.conj(z)*z))
        
              for l in xrange(L): #UPDATE y
                  pq = PQ[str(l)]
                  num = 0
                  den = 0
                  for k in xrange(len(pq)): #loop through all baselines for each redundant spacing
                      p = pq[k][0]
                      q = pq[k][1]

                      num = num + np.conjugate(g_old[p])*g_old[q]*D[p,q]
                      den = den + np.absolute(g_old[p])**2*np.absolute(g_old[q])**2
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
 
      def read_in_D(self,ms_file):
          os.chdir(it.PATH_DATA)
          N = len(it.ANT_ID)
          B = (N**2 + N)/2 #ASSUMING THE FILE CONTAINS AUTOCORRELATIONS

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
                  flag_row_mat[k,j,:] = flag_row[temp_indx]
                  indx_2d = indx_1d[temp_indx] 

          #print "data_chunck = ",data_chunck.shape
          #print data.shape
          #print flag.shape

          os.chdir(it.PATH_CODE)
          return data_mat,flag_mat,flag_row_mat,indx_2d
 
      def apply_redundant_stefcal(self,ms_file):
          os.chdir(it.PATH_DATA)
          data_mat,flag_mat,flag_row_mat, indx_2d = self.read_in_D(ms_file)
          ant = self.hex_grid(hex_dim=2,l=14.6)
          #plt.plot(ant[:,0],ant[:,1],'bo')
          #plt.show()
          phi,zeta,L = self.calculate_phi(ant[:,0],ant[:,1])
          plt.imshow(phi)
          plt.show()
          PQ = self.create_PQ(phi,L)
          #print "PQ = ",PQ
          plt.imshow(np.absolute(data_mat[:,:,25,701]-data_mat[:,:,25,701]*np.eye(19)))
          plt.show()
          z_temp,converged,G,M,start,stop,i,error_vector = self.redundant_StEFCal(D=data_mat[:,:,25,701],phi=phi,tau=1e-9,alpha=1.0/3.0,max_itr=1000,PQ=PQ)
          print "converged = ",converged
          plt.imshow(np.absolute(M))
          plt.show()
          plt.imshow(np.absolute(data_mat[:,:,25,701]*G**(-1)-data_mat[:,:,25,701]*np.eye(19)*G**(-1)))
          plt.show()

          plot_before_after_cal_per_t_f(data_mat[:,:,25,701],G,phi)
          os.chdir(it.PATH_CODE)

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

if __name__ == "__main__":
   red_cal = redundant_stefcal()
   os.chdir(it.PATH_DATA)
   file_names = glob.glob("*uvcUC.ms")
   os.chdir(it.PATH_CODE)
   red_cal.apply_redundant_stefcal(file_names[0])

   #data_mat,flag_mat,flag_row_mat, indx_2d = red_cal.read_in_D(file_names[0])

   #plt.plot(data_mat[0,3,30,:])
   #plt.show()

