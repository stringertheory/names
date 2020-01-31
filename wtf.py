import sys

from multiprocessing import Pool

N = 2

def f(index):
    print index
                
if __name__ == '__main__':

    pool = Pool(N)
    pool.map(f, range(N))
    
