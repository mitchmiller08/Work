
#################################################
##  Formats GIXOS data for use in Motofit.     ##
##  Copy this file into directory with raw     ##
##  GIXOS data to be processed. Specify files  ##
##  to be removed below. Run command:          ##
##  >>python GIXOS_proc.py                     ##
##  All files will be processed creating files ##
##  with paths "'original path'_p.txt"         ##
##  Three columns:  1. Q_z, 2. Intensity,      ##
##  3. Error (set to zero)                     ##
#################################################


import sys
import numpy as np
import math as m
import os

def getFiles():
    
    paths = [f for f in os.listdir('.') if os.path.isfile(f)]
    ##  Files to be removed (any extra files in directory not to be processsed
    paths.remove('GIXOS_proc.py')   ## Remove this file from list
    paths.remove('patterson.py')
    paths.remove('.DS_Store')   ## Remove OS X formatting file

    return paths

def readFile(path):
    data = np.loadtxt(path)
    qVals, signal, back = np.split(data,3,axis=1)
    
    return qVals,signal, back

def processData(qVals,signal,back):
    qc = 0.01029
    n = np.size(qVals)
    data = signal - back
    ref = back
    for i in range(0,n):
        if qVals[i] < qc:
            ref[i] = 0
        else:
            ref[i] = ((qVals[i] - m.sqrt(qVals[i]**2 - qc**2))/(qVals[i] + m.sqrt(qVals[i]**2 - qc**2)))**2
    data = data * ref
    error = np.zeros((n,1))
    data = np.concatenate((qVals,data,error),axis=1)
    data = data[data[:,0] > qc]     ## Remove values below Q_c

    return data

def outputData(path,data):
    name,extension = path.split('.')
    outPath = name + '_p.' + extension
    np.savetxt(outPath,data,fmt='%.8f',delimiter='     ')

### Begin Main
paths = getFiles()

for path in paths:
    qVals,signal,back = readFile(path)
    data = processData(qVals,signal,back)
    outputData(path,data)
