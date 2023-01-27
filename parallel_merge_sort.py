
from random_file_gen import random_binary_unique
import time
import multiprocessing
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def bsm(x, arr, low, high):
    if(low==high):
        if(arr[low] <x):
            return low+1
        else:
            return low
    else:
        mid = (low+high)//2
        if(x>arr[mid]):
            if(mid == high):
                return bsm(x, arr, mid, high)
            else:
                return bsm(x, arr, mid+1, high)
        else:
            if(low == mid):
                return bsm(x, arr, low, mid)
            else:
                return bsm(x, arr, low, mid-1)


# print(bsm(40,[25,35,45,67,78], 0,4))
import array
def mas(*args):
    arr1 = args[0][0]
    arr2 = args[0][1]
    # res = shared_memory.SharedMemory(name=args[0][2])
    res = args[0][2]
    # res = np.ndarray(arr.shape, arr.dtype, buffer = shm_a.buf)
    # array.array('bres', res.buf)
    for i in range(len(arr1)):
        pos = bsm(arr1[i], arr2, 0, len(arr2)-1)
        res[pos+i] = int(arr1[i])
    # return res

# mas([20,30,40,50, 100, 111, 199],[25,35,45,67,78, 2000],[0,0,0,0,0,0,0,0,0, 0, 0, 0, 0])
import sys

def mergeArrayBs(*args):
    left, right, a = args[0] if len(args) == 1 else args
    executor = ThreadPoolExecutor()
    payl = [[left, right, a], [right, left, a]]
    executor.map(mas, payl)
    executor.shutdown()

def merge(*args):
    # Support explicit left/right args, as well as a two-item
    # tuple which works more cleanly with multiprocessing.
    left, right = args[0] if len(args) == 1 else args
    left_length, right_length = len(left), len(right)
    left_index, right_index = 0, 0
    merged = []
    while left_index < left_length and right_index < right_length:
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    if left_index == left_length:
        merged.extend(right[right_index:])
    else:
        merged.extend(left[left_index:])
    return merged


import math
import threading
def parallel_mergeSort(arr, processes):
    lengthArr = len(arr)
    # divs = lengthArr//(multiprocessing.cpu_count()/2)
    threads = threading.active_count()
    if(len(arr) == 1 or len(arr) == 0):
        return arr
    else:
        m = int(len(arr)/2)
        s1 = parallel_mergeSort(arr[:m], processes)
        s2 = parallel_mergeSort(arr[m:], processes)
        
        if( processes>threads):
            # shm_a = shared_memory.SharedMefmory(create=True, size=lengthArr*4)
            a = np.zeros([lengthArr], dtype=int)
            cm_time_star = time.time()

            mergeArrayBs([s1, s2, a])
            cm_time_endd = time.time()
            cm_tim = cm_time_endd - cm_time_star
            # print("parallel chunk sort time = %f" %cm_tim, "for data size", lengthArr)
            # print(a)
            res = a
        else:
            res = merge(s1, s2)

    # print(len(res))
    return res


# # #@profile
# def pms(data): 
    
#     processes = multiprocessing.cpu_count()
#     pool = multiprocessing.Pool(processes=processes)
#     # print("before merge length", len(data))

#     size = int(math.ceil(float(len(data)) / processes)) 
#     data = [data[i * size:(i + 1) * size] for i in range(processes)]
#     # ress =  pool.apply_async(mergeSort, partitionedData)
#     data = pool.map(parallel_mergeSort, data)
#     # res = []
#     while len(data) > 1:
#         extra = data.pop() if len(data) % 2 == 1 else None
#         data = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
#         data = pool.map(mergeArrayBs, data) + ([extra] if extra else [])
#     return data[0]

def run_pms(data,cores):
    # data = []
    # with open(input_file_name, 'rb') as f:
    #     for _ in range(0, int(num)):
    #         block = f.read(4)
    #         list = [int.from_bytes(block, byteorder='little', signed=True)]
    #         data += list   
    processes = multiprocessing.cpu_count()
    if(cores< processes):
        processes = cores    
    else:
        print("Limiting cores to cpu limit", processes)
    cm_time_sta = time.time()

    res = parallel_mergeSort(data, processes)
    cm_time_end = time.time()
    cm_tim = cm_time_end - cm_time_sta
    print("parallel Merge sort time(sec) = %f" %cm_tim)

    return res
    
    


if __name__ == '__main__':
    input_file_name = './exercise02/input.dat'
    output_file_name = './exercise02/outputpms.dat'
    print("Please enter random numbers length")
    num = int(input())
    print("Please enter number of cores")
    cores = int(input())
    random_binary_unique(num, input_file_name)
    run_pms(num,cores, input_file_name, output_file_name)






