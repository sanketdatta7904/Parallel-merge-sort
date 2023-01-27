
# THis program is to test the sanity of the external merge sort with comparison of classic merge sort

from mergesort import cms
from random_file_gen import random_binary_unique
import numpy as np
import copy
# from external_mergesort import external_merge_sort as ems
from parallel_merge_sort import run_pms

from quickSort import quickSort

# import external_mergesort



def test_file(num):
    
    print("Enter number of cores")
    cores = int(input())

    # ram_available = psutil.virtual_memory().available
    # print("Total ram available", ram_available/(1024*1024), "mb")
    # print("Will be testing with ", num, "numbers")
    import time
    inputFileName = './exercise02/input.dat'
    random_binary_unique(num, inputFileName)

    data = []
    with open(inputFileName, 'rb') as f:
        for _ in range(0, int(num)):
            block = f.read(4)
            list = [int.from_bytes(block, byteorder='little', signed=True)]
            data += list


    # Testing classical merge sort
    cm_time_sta = time.time()
    res_cms = cms(data)
    cm_time_end = time.time()
    cm_tim = cm_time_end - cm_time_sta
    print("classic Merge sort time(sec) = %f" %cm_tim)

    # Testing External merge sort
   
    res_pms =run_pms(data,cores)
    print("Record count of classic merge sort", res_cms)
    print("Record count of Parallel merge sort", res_pms)
    # matchedCount = 0
    # notMatchedCount = 0
    print("matching",(res_cms == res_pms).all())
print("Testing with data size of 1000")
num = 1000
test_file(num)