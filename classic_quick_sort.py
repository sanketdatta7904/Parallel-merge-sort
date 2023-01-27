def swap(arr, a, b):
    temp = arr[b]
    arr[b] = arr[a]
    arr[a] = temp

    return arr
    
def rearrange(arr, start_index, end_index):
    
    pivot = arr[start_index]
    pivot_index = start_index
    for i in range(start_index, end_index+1):
        if(arr[i] < pivot):
            pivot_index = pivot_index + 1
    swap(arr, start_index, pivot_index)
       
    si = start_index
    ei = end_index
    while(si < ei):
        if(arr[si] < pivot):
            si = si + 1
        elif(arr[ei]>=pivot):
            ei = ei - 1
        else:
            swap(arr, si, ei)
            si = si + 1
            ei = ei - 1
    
    return pivot_index    
    
def classic_quick_sort(data, start_index, end_index):
    
    print(data, start_index, end_index)
    if (start_index >= end_index):
        return data
    else:
        pivot_index = rearrange(data, start_index, end_index)
        data  = classic_quick_sort(data, start_index, pivot_index-1)
        data  = classic_quick_sort(data, pivot_index + 1, end_index)
    return data
        

def cqs(num, inputFileName, outputFileName):

    data = []
    with open(inputFileName, 'rb') as f:
        for _ in range(0, int(num)):
            block = f.read(4)
            list = [int.from_bytes(block, byteorder='little', signed=True)]
            data += list
    print(data)
    return
    classic_quick_sort(data, 0, len(data))
    print(data)


if __name__ == '__main__':
    DATA = [6, 15,4, 2, 8, 5, 11, 9, 7, 13]
    
    print(f"{DATA} -> {classic_quick_sort(DATA, 0, len(DATA)-1)}")









