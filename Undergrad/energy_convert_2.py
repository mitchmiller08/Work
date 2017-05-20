import os


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

## Builds a list of data points after "DATA:"
for line in lines:
    line = line.strip()
    if data_flag == True:
        data_list.append(line)
        
    else:
        outfile.write(line)
        
    if line == "DATA:":
        data_flag = True
        outfile.write("Counts\tEnergy\n")
        
## Converts counts to energy
for channel in data_list:
    outfile.write("TEST\n")
    if quad == 0:
        energy = channel * slope + offset
        
    else:
        energy = slope * channel ** quad + offset
        
    string = []
    string = str(channel),'\t',str(energy),'\n'
    out = ''.join(string)
    outfile.write(out)
    
infile.close()
outfile.close()
