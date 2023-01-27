import numpy.random as random
import os
import sys
import numpy as np


def random_binary_unique(num, input_file_name):
    file = open(input_file_name, 'wb') 
    print("Generating file with random numbers count", num)
    min = 1
    max = 1001
    tot = num
    # b= np.array([])
    while(num>0):
        
        if(num<1000):
            size = num
        else:
            size = 1000
        a = random.choice(range(min, max), size, replace=False)
        for i in range(0, len(a)):
            # b = np.append(b,a[i])
            file.write(int(a[i]).to_bytes(4, signed=True, byteorder='little'))
        min = min+1001
        max = max+1001
        num = num-1000
    file.close()
    # print(b)
    arr = np.array([])
    # with open(input_file_name, 'rb') as test_file:
    #     for j in range(0, tot):
    #         tblock = test_file.read(4)
    #         enum = int.from_bytes(tblock, byteorder='little')          
    #         arr = np.append(arr,enum)   
        # print(arr)
        # print("Length of array>>", len(arr))
    print("File creation completed")
    # print("matching",(b == arr).all())
    print("random filesize",os.path.getsize(input_file_name)/(1024*1024), "mb") 
# random_binary_unique(10000)

