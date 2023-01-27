#!/usr/bin/env python
# coding: utf-8


import multiprocessing
import math
import itertools
import time
import random

def make_bin_wide(bin_num, split_num):

    bin_wide = [bin_num // split_num for i in range(split_num)]
    quotient = bin_num // split_num
    remainder = bin_num - quotient * split_num
#    print("make_bin_wide: bin_num, split_num, quotient, remainder:", bin_num, split_num, quotient, remainder)

    for i in range(split_num):
        if remainder > 0:
            bin_wide[i] = bin_wide[i]  + 1
            remainder = remainder - 1
        else:
            break
    
    return bin_wide

def swap(arr, a, b):
    if(len(arr) > 1):
        temp = arr[b]
        arr[b] = arr[a]
        arr[a] = temp
    return arr

def local_rearrange(pivot, arr):
    si = 0
    ei = (len(arr) - 1)
#    print("local", pivot, arr)
    
    while(si < ei):
        if(arr[si] < pivot):
            si = si + 1
        elif(arr[ei]>=pivot):
            ei = ei - 1
        else:
            swap(arr, si, ei)
            si = si + 1
            ei = ei - 1

    count_small = 0
    pivot_index = -1
    for i in range(0, len(arr)):
        if arr[i] < pivot:
            count_small = count_small + 1
        if arr[i] == pivot:
            pivot_index = i
        else:
            continue    
    
    if pivot_index >= 0:
        _ = arr.pop(pivot_index)
    
    return count_small, arr

def wrap_local_rearrange(arr):
    ei = arr.pop(len(arr)-1)
    si = arr.pop(len(arr)-1)
    pivot = arr.pop(len(arr)-1)
    count_small, arr = local_rearrange(pivot, arr[si:ei])
    arr.append(count_small)
    return  arr
        
def rearrange(arr, start_index, end_index):
    NO_PARALLEL = 32
#    print("rearrange: start_index, end_index, arr", start_index, end_index, arr)
    
    org_arr = arr.copy()
    
    arr = arr[start_index:(end_index+1)].copy()    
    pivot = arr.pop(0)
    pivot_index = 0
    for i in range(0, len(arr)):
        if(arr[i] < pivot):
            pivot_index = pivot_index + 1

    if (end_index - start_index) <= NO_PARALLEL :
        count_small, arranged_arr = local_rearrange(pivot, arr)

        arr = org_arr.copy()
        arr[start_index: (start_index + count_small)] = arranged_arr[0:count_small]
        arr[start_index+count_small] = pivot
        arr[start_index+count_small+1:end_index+1] = arranged_arr[count_small:]

        return arr, start_index + pivot_index


            
    pool = multiprocessing.Pool(processes=4)
        
    new_arr = []
    bin_wide = make_bin_wide((end_index - start_index), 4)
    bin_index = []
    bin_index.append(0 + start_index)
    for i in range(4):
        bin_index.append(bin_index[i] + bin_wide[i])  
        
    for i in range(4):
        tmp_arr = org_arr.copy()
        tmp_arr.pop(0)
        si = bin_index[i]
        ei = bin_index[i+1]
            
        tmp_arr.append(pivot) 
        tmp_arr.append(si)
        tmp_arr.append(ei)
        new_arr.append(tmp_arr)
         
    local_arranged_arr = pool.map(wrap_local_rearrange, new_arr)
    pool.close()
        
    count_small = []
    for i in range(4):
        count_small.append(local_arranged_arr[i].pop(len(local_arranged_arr[i])-1))
            
    small_arr = []
    for i in range(4):
        tmp_count_small = count_small[i]
        if tmp_count_small == 0:
            continue
        tmp_arr = local_arranged_arr[i][0:tmp_count_small]
        small_arr = small_arr + tmp_arr
 
    big_arr = []
    for i in range(4):
        tmp_count_small = count_small[i]
        if (len(local_arranged_arr[i]) - tmp_count_small) == 0:
            continue
        tmp_arr = local_arranged_arr[i][tmp_count_small:]
        big_arr = big_arr + tmp_arr
             
    arr = org_arr.copy()

    if (len(small_arr)) > 0:
        arr[start_index:start_index + len(small_arr)] = small_arr[0:len(small_arr)]
    
    arr[start_index+len(small_arr)] = pivot
    
    if (len(big_arr)) > 0:
        arr[start_index+len(small_arr)+1:start_index+len(small_arr)+1+len(big_arr)] = big_arr[0:len(big_arr)]

    return arr, start_index + pivot_index    

def partial_parallel_quick_sort(data, start_index, end_index):

    # print("\n\n #### NEW STEP ###\n start_index, end_index, len(data): " + str(start_index) + ", " + str(end_index) +  ", " +  str(len(data)) + "\n\n")

#    print("data:", data)
        
    if (start_index >= end_index):
        return data
    else:
        data, pivot_index = rearrange(data, start_index, end_index)
#        print("Global", data)
#        print("\n## Left ##\n")
        data  = partial_parallel_quick_sort(data, start_index, pivot_index-1)
#        print("\n## Right ##:\n")
#        print("Right input data:", data)
        data  = partial_parallel_quick_sort(data, pivot_index+1 , end_index)
        
#    print("return data:", data)
    return data

def wrap_partial_parallel_quick_sort(data):

    end_index = data.pop(len(data)-1)
    start_index = data.pop(len(data)-1)

    data = partial_parallel_quick_sort(data, start_index, end_index)
    
    return  data

def parallel_quick_sort(data, start_index, end_index):
#    print("\n\n #### First STEP ###\n start_index, end_index, len(data): " + str(start_index) + ", " + str(end_index) + ", " +  str(len(data)) + "\n\n")
#    print("data:", data)
    
    depth = 0
    data, pivot_index = rearrange(data, start_index, end_index)
    pivot = data[pivot_index]
        
    new_data = []
    for i in range(2):
        tmp_data = data.copy()
        if i == 0:
            si = 0
            ei = pivot_index - 1
        elif i == 1:
            si = pivot_index + 1
            ei = end_index
        
        tmp_data.append(si)
        tmp_data.append(ei)
        new_data.append(tmp_data)
 
    pool0 = multiprocessing.Pool(processes=2)
    data_parallel = pool0.map(wrap_partial_parallel_quick_sort, new_data)
    pool0.close()

    data0 = data_parallel[0]
    data1 = data_parallel[1]

#    print("data0", data0)
    
    final_data = []
    for i in range(0, pivot_index):
        final_data.append(data0[i])
    final_data.append(pivot)
    for i in range(pivot_index+1, end_index+1):
        final_data.append(data1[i])
    
    return final_data

def pqs(num, inputFileName, outputFileName):

    data = []
    with open(inputFileName, 'rb') as f:
        for _ in range(0, int(num)):
            block = f.read(4)
            list = [int.from_bytes(block, byteorder='little', signed=True)]
            data += list

    f.close()
    parallel_quick_sort(data, 0, len(data))
    
if __name__ == '__main__':
#    DATA = [14,9,3,15,7,1,17,11,6,10,8,5,13,12,16,20,18,2,19,4]
#    DATA = [6, 15,4, 2, 8, 5, 11, 9, 7, 13]
#    DATA = [36,9,37,71,43,94,67,49,80,76,99,52,88,72,54,74,86,33,90,11,82,39,42,98,59,83,69,26,15,3,50,13,0,78,31,30,91,1,51,87,8,19,61,62,44,10,70,48,85,66,32,17,58,46,20,18,60,64,65,89,34,92,100,7,4,22,27,16,63,47,40,53,79,25,14,28,57,21,68,56,96,41,5,24,23,93,84,95,77,73,2,97,81,35,75,55,29,45,6,12]
    DATA = list(range(1000))
    print(DATA)
    random.shuffle(DATA)
    print(DATA)
    time_sta = time.time()
#    print(f"{DATA} -> {partial_parallel_quick_sort(DATA, 0, len(DATA)-1)}")
    print(f"{DATA} -> {parallel_quick_sort(DATA, 0, len(DATA))}")
    time_end = time.time()
    my_time = time_end - time_sta
    print("Parallel Quick sort time(sec) = %f" %my_time)











