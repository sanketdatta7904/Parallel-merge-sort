
# THis program is to test the sanity of the external merge sort with comparison of classic merge sort

from random_file_gen import random_binary_unique
import sys
import psutil
import math
import numpy as np
import multiprocessing
import copy
# from external_mergesort import external_merge_sort as ems
from quickSort import quickSort

from parallel_quick_sort import parallel_quick_sort
# import external_mergesort



def test_file(num):
    
    import time
    inputFileName = './exercise02/inputqs.dat'
    # outputFileNameCms = './exercise02/outputcqs.dat'
    # outputFileNamePms = './exercise02/outputpqs.dat'

    random_binary_unique(num, inputFileName)


    data = []
    with open(inputFileName, 'rb') as f:
        for _ in range(0, int(num)):
            block = f.read(4)
            list = [int.from_bytes(block, byteorder='little', signed=True)]
            data += list

    copyData = copy.deepcopy(data)
    # print(copyData)
    # Testing classical quick sort
    cm_time_sta = time.time()
    quickSort(copyData, 0, len(data)-1)
    cm_time_end = time.time()
    cm_tim = cm_time_end - cm_time_sta
    print("classic Quick sort time(sec) = %f" %cm_tim)

    # Testing Parallel quick sort
    cm_time_sta = time.time()
    data = parallel_quick_sort(data, 0, len(data)-1)
    cm_time_end = time.time()
    cm_tim = cm_time_end - cm_time_sta
    print("Parallel Quick sort time(sec) = %f" %cm_tim)
    print(data)
    print(copyData)
    # matchedCount = 0
    # notMatchedCount = 0
    print("matching both result>>>",(data == copyData))
    # for i in range (0, len(cm_list)-1):
    #     if(cm_list[i] == pm_list[i]):
    #         matchedCount += 1
    #     else:
    #         notMatchedCount +=1

    # print({"matchedCount": matchedCount, "notMatchedCount": notMatchedCount})
if __name__ == '__main__':

    print("Testing with random numbers of length 10000")
    num = 10000
    test_file(num)