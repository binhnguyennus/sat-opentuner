import os
import time
from subprocess import call
from multiprocessing import Pool, cpu_count

EXEC_DIR = 'sat-opentuner'
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

if __name__ == '__main__':
    PROJECT_DIR = os.getcwd().split(EXEC_DIR)[0]
    os.chdir(PROJECT_DIR + EXEC_DIR)
    with open(INSTANCES, 'r') as instance_file:    
        lines = instance_file.read().splitlines()

    pool = Pool(cpu_count())
    for line in lines:
        pool.apply_async(ccanr_glucose, args=(INSTANCES_DIR + line, ))

    pool.close()
    pool.join()
