import os
import sys


## Initialize Variables
filepath = raw_input()
infile = open(filepath, 'r')
outfile = open(filepath.replace(".","_energy."),'w')
data_list = []
data_flag = False
lines = infile.readlines()

## Read in offset, slope, and quadratic values
offset_list = lines[7].split()
offset = float(offset_list[1])
slope_list = lines[8].split()
slope = float(slope_list[1])
quad_list = lines[9].split()
quad = float(quad_list[1])

## Build a list of data points after "DATA:"
## and convert to energy
for line in lines:
    line = line.strip()
    if data_flag == True:
        if quad == 0:
            energy = float(line) * slope + offset
        else:
            energy = slope * float(line) ** quad + offset
        string = []
        string = line,'\t',str(energy),'\n'
        out = ''.join(string)
        outfile.write(out)

    ## Write header info to new file    
    else:
        outfile.write(line)
        outfile.write('\n')
        
    if line == "DATA:":
        data_flag = True
        outfile.write("Counts\tEnergy\n")
    
infile.close()
outfile.close()
