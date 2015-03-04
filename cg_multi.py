import os
import time
from subprocess import call
from multiprocessing import Pool, cpu_count

SOLVERS_DIR = 'solvers/'
INSTANCES_DIR = 'instances/sat_lib/'
INSTANCES = 'instance_set_3.txt'

def ccanr_glucose(filename): 

    cmd = SOLVERS_DIR + 'CCAnrglucose/CCAnr+glucose.sh '
    instance = filename
    args = ' 1 1000'
    #print cmd + instance + args
    #call(cmd + instance + args, shell=True)
    call(cmd + instance + args, stdout=open(os.devnull, 'wb'), shell=True)
    return

def cb(one):
    print 'oi\n'

with open(INSTANCES, 'r') as instance_file:    
    lines = instance_file.read().splitlines()

#complete_lines = lines
#lines[:] = [INSTANCES_DIR + l for l in lines]

if __name__ == '__main__':
    pool = Pool(cpu_count())
    #result = pool.map_async(ccanr_glucose, lines)
    #result.get()
    for line in lines:
        pool.apply_async(ccanr_glucose, args=(INSTANCES_DIR + line, ))

    pool.close()
    pool.join()
