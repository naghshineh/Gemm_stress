import threading
import argparse
import sys
import random
from numpy import *
import time

parser=argparse.ArgumentParser()
parser.add_argument("--size", help="enter amount in MB of memory to occupy", type=int)
parser.add_argument("--loop", help="enter how many times to loop", type=int)
parser.add_argument("--copies", help="enter how many copies to spawn", type=int)
parser.add_argument("--int", help="Multiplies a matrix of integers", action="store_true")
parser.add_argument("--float", help="Multiplies a matrix of floats", action="store_true")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args=parser.parse_args()

# Matrix multiply function that generates random matrix to fill the size in MB
# The multipy also repeats itself based on repeat argument. num here is the thread number
def mmul(size, repeat, num):
	start_time = time.time()
	print('Hog %d : Generating matrix...' % num )

	n_raw = (size*1024*1024)/16
	n_sqrt = math.sqrt(n_raw)
	n = int(round(n_sqrt)) + 1
	n2 = n*n
	if (args.float):
		x = random.rand(n2)
		y = random.rand(n2)
	if (args.int):
		x = random.randint(10, size=n2)
		y = random.randint(10, size=n2)
	reshape(x,(n,n))
	reshape(y,(n,n))
		
	print('Hog %d : Multiplying matrices...' % num )
	for p in range(0, repeat):
		matmul(x, y)
	elapsed_time = time.time() - start_time
	if (args.float):
		print ('Hog %d : Completed in %f seconds multiplied %dMB of floatingpoint data' % (num,elapsed_time, (2*int(sys.getsizeof(x)/(1024*1024))) ))
	if (args.int):
		print ('Hog %d : Completed in %f seconds multiplied %dMB of integer data' % (num,elapsed_time, (2*int(sys.getsizeof(x)/(1024*1024))) ))

def worker(num):
	mmul(args.size, args.loop,num)

threads = []
print "\nDispatching worker Hogs\n-----------------------"
for i in range(args.copies):
	t = threading.Thread(target=worker, args=(i,))
	threads.append(t)
	t.start()
