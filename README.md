
Setting up the environment:

apt-get update
apt-get install build-essential
pip3 install memory-profiler requests
pip3 install numpy
pip3 install psutil



C.  Testing the Sanity of both programs:
We used two different test case to test the accuracy of the programs. We tested with around 1000 numbers to test the accuracy of both programs. 
1. Testing merge sort

run
python exercise02/testFilemergesort.py 

After this, please enter how many cores to be used 

- It will generate 1000 random integers file and then test both programs and then compare the result in the end. 

2. Testing quick sort
run
python -O exercise02/testfilequicksort.py  - It will generate 1000 random integers file and then test both programs and then compare the result in the end. 

   
Command for testing the individual files:

Parallel Merge sort:
run
python exercise02/parallel_merge_sort.py 
then enter:
>how many numbers to be tested
>how many cores to be used

Parallel Quick sort:

python -O exercise02/parallel_quick_sort.py
then enter:
how many numbers to be tested
(number of core for rearrange is 4 and recursion is 2  (Hard-corded))

