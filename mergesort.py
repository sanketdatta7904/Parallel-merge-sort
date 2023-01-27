
from random_file_gen import random_binary_unique
import time
import sys
import psutil

# random_binary()




def mergeArray(s1, s2):
    a = 0
    b = 0
    arr = []
    while(a < len(s1) and b < len(s2)):
        if(s1[a] > s2[b]):
            arr.append(s2[b])
            b = b+1
        elif(s1[a] <= s2[b]):
            arr.append(s1[a])
            a = a+1
    if(a == len(s1)):
        arr.extend(s2[b:])
    elif(b == len(s2)):
        arr.extend(s1[a:])
    
    return arr

def mergeSort(arr):
   
    if(len(arr) == 1 or len(arr) == 0):
        return arr
    else:
        m = int(len(arr)/2)
        s1 = mergeSort(arr[:m])
        s2 = mergeSort(arr[m:])
        if(len(s1)>=200000 and len(s2) >= 200000):
            print("nowww")
        res = mergeArray(s1, s2)
    return res

#@profile
def cms(data):
    

    abc = mergeSort(data)

    return abc


#@profile
def run(num):
    
    # Success
    # num = 32768; """For 0.125 mb file"""
    
    # Success
    # num = 1048576; """For 4 mb file"""

    # Failed
    # num = 2097152; """For 8 mb file"""

    ram_available = psutil.virtual_memory().available
    # print("Total ram available", ram_available/(1024*1024), "mb")
    print("Will be testing with ", num, "numbers")
    
    random_binary_unique(num)

    cm_time_sta = time.time()

    cms(num, './exercise02/input.dat', './exercise02/X1.dat')

    cm_time_end = time.time()
    cm_tim = cm_time_end - cm_time_sta
    print("classic Merge sort time(sec) = %f" %cm_tim)


# num = int(input())
if __name__ == '__main__':
    num = int(input())
    run(num)




