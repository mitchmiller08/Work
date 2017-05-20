import os
import sys



if sys.argv:
    filepath = sys.argv

for path in filepath[1:]:
    ## Initialize Variables
    infile = open(path, 'r')
    outfile = open(path.replace(".","_energy."),'w')
    data_list = []
    data_flag = False
    channel = 0
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
                energy = channel * slope + offset
            else:
                energy = slope * float(line) ** quad + offset
            string = []
            string = str(energy),'\t',line,'\n'
            out = ''.join(string)
            outfile.write(out)
            channel = channel + 1

        if line == "DATA:":
            data_flag = True
            outfile.write("DATA:\tEnergy (kev)\tCounts\n")

        ## Write header info to new file    
        if data_flag == False:
            outfile.write(line)
            outfile.write('\n')
            
    
    infile.close()
    outfile.close()
