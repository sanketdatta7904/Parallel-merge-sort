
def swap(arr, a, b):
    temp = arr[b]
    arr[b] = arr[a]
    arr[a] = temp


def partition(arr, s, e):
    a = arr[s]
    cout = 0
    for i in range (s, e+1):
        if(arr[i]<a):
            cout = cout +1
    cout = s+cout
    swap(arr, s, cout)
    si = s
    ei = e
    while(si<ei):
        if(arr[si]<a):
            si = si +1
        elif(arr[ei]>=a):
            ei = ei-1
        else:
            swap(arr, si, ei)
            si = si +1
            ei = ei-1
    # print(cout)
    return cout



def quickSort(arr, s, e):
    if(s>=e):
        return
    else:
        pivot = partition(arr, s, e)
        quickSort(arr, s, pivot-1)
        quickSort(arr, pivot+1, e)




# a = [100,99,67,32]
# quickSort(a, 0, 3)

# print(a)
