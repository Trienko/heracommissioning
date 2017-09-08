import glob
import os
from ephem import *
import pickle
import numpy as np
import pylab as plt

def plot_lst_range():
    HERA = Observer()
    HERA.lat, HERA.long, HERA.elevation = '-30:43:17', '21:25:40.08', 0.0
    j0 = julian_date(0)
    dict_lst = pickle.load(open("save.p", "rb"))

    days = np.array(dict_lst.keys())

    dir_numbers = np.zeros((len(dict_lst.keys()),))
    file_numbers = np.zeros((len(dict_lst.keys()),))
    #max_lst = np.zeros((len(dict_lst.keys()),))
    #min_lst = np.zeros((len(dict_lst.keys()),))

    lst_matrix = np.zeros((24,len(days)))
    
    k = 0
    for day in days:
        dir_numbers[k] = int(day)
        k += 1

    idx = np.argsort(dir_numbers)
    dir_numbers = dir_numbers[idx]
    days = days[idx]       

    k = 0
    #print "dict_lst.keys = ",dict_lst.keys
    for key in days:
        file_names = dict_lst[key]
        print "key = ",key
        #k = k + 1
        i = 0
        ra_cen = np.zeros((len(file_names),))
        file_numbers[k] = len(file_names)
        for file_name in file_names:
            print "file_name = ",file_name
            file_name = file_name[2:]
            file_name_split = file_name.split('.')
            lst = file_name_split[1]+'.'+file_name_split[2]
            HERA.date = float(lst) - j0
            ra_cen[i] = float(HERA.sidereal_time())
            temp_v = int(ra_cen[i]*(12/np.pi))
            lst_matrix[temp_v,k] += 1 
            i = i + 1
            print "MSNAME: %s, UTC: %s (LST %s = %f)" % (file_name, HERA.date, HERA.sidereal_time(), float(HERA.sidereal_time()) )
        #if len(ra_cen) > 0:
        #   max_lst[k] = np.amax(ra_cen)
        #   min_lst[k] = np.amin(ra_cen)
        k = k + 1
    lst_matrix[lst_matrix>1] = 1
    #print "dir_number = ", dir_numbers
    #plt.plot(dir_numbers,max_lst*(12/np.pi),'ro')
    #plt.plot(dir_numbers,min_lst*(12/np.pi),'bo')  
    #print "dict_lst.keys = ",dict_lst.keys()  
    #plt.show()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(lst_matrix,aspect='auto')
    one = np.ones((len(days),))
    x = np.cumsum(one)-1
    ax.plot(x,one*6,"r--",linewidth=2.0)
    ax.plot(x,one*10,"r--",linewidth=2.0)
    ax.plot(x,one*21,"k",linewidth=2.0)
    ax.plot(x,one*18,"k",linewidth=2.0)
    x_copy = np.copy(x)
    x = days.tolist().index("2457661")
    #y = [0,24]
    #ax.plot(x,y,'c',linewidth=2.0)
    ax.axvline(x=x)
    x = days.tolist().index("2457555")
    ax.axvline(x=x)
    x = days.tolist().index("2457545")
    ax.axvline(x=x)
    ax.set_ylabel("LST [h]")
    ax.set_xlabel("JD")
    ax.set_title("HERA-19 LST RANGE [xx]")
    idx = np.array([0,0,50,100,150,200,250])
    labels = days[idx]
    print "labels = ",labels
    #labels = [item.get_text() for item in ax.get_xticklabels()]
    #labels = np.array(["12$^h$","10$^h$","8$^h$","6$^h$","4$^h$","2$^h$","0$^h$","22$^h$","20$^h$","18$^h$","16$^h$","14$^h$","12$^h$"])
    ax.set_xticklabels(labels)
    #plt.colorbar()
    #fig.canvas.draw()
    #ax.plot([2457661,2457661],[0,24],'c',linewidth=4.0)
     
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x_copy,file_numbers,'bo')
    ax.set_xticklabels(labels)
    plt.show()         
    

'''
PATH_DATA = "/data4/paper/HERA2015/"

def plotting_file_numbers_per_JD():
    dir_names = glob.glob(PATH_DATA+"2*")
    dir_numbers = np.zeros((len(dir_names),))
    dir_count = np.zeros((len(dir_names),))
    k = 0

    for dir_name in dir_names:
        if os.path.isdir(PATH_DATA+dir_name):
           dir_numbers[k] = int(dir_name)
           file_names = glob.glob(PATH_DATA+dir_name+"/*xx*HH*uvc") 
           dir_count[k] = len(file_names)
           k = k + 1

    idx = np.argsort(dir_numbers)
    dir_names = dir_names[idx]
    dir_number = dir_numbers[idx]
    dir_count = dir_count[idx]
    k = 0
    for dir_name in dir_names:
        print "######################################################"
        print "JD:: "+dir_name
        print "Number of snapshots:: "+dir_count[k]
        print_lst(print_values=True,dir_name=dir_name)
        k += 1
        print "######################################################"
         

def print_lst(self,print_values=False,dir_name=""):
    #print PATH_DATA
    #os.chdir(PATH_DATA)
    HERA = Observer()
    HERA.lat, HERA.long, HERA.elevation = '-30:43:17', '21:25:40.08', 0.0
    j0 = julian_date(0)
    
    file_names = glob.glob(PATH_DATA+dir_name+"/*xx*HH*uvc")
    file_numbers = np.zeros((len(file_names),))
    k = 0    
    for file_name in file_names:
        file_name_split = file_name.split('.')
        file_numbers[k] = float(file_name_split[1]+'.'+file_name_split[2])
        k += 1

    idx = np.argsort(file_numbers)
    file_names = file_names[idx]

    ra_cen = np.zeros((len(file_names),))
    k = 0 
    for file_name in file_names:
        file_name_split = file_name.split('.')
        lst = file_name_split[1]+'.'+file_name_split[2]
        HERA.date = float(lst) - j0
        ra_cen[k] = float(HERA.sidereal_time())
        k = k + 1
        if print_values:
           print "MSNAME: %s, UTC: %s (LST %s = %f)" % (file_name, HERA.date, HERA.sidereal_time(), float(HERA.sidereal_time()) )
'''

if __name__ == "__main__":
   plot_lst_range()
