#Mitchell Miller
#Data conversion utility

#Change file paths to desired

input = open('C:\Users\Mitch\Documents\Segre files\mca_spect.0079','r')
output = open('C:\Users\Mitch\Documents\Segre files\mca_spect_energy.0079','w')
x = 0
while x<18:             #reads through header info
    input.readline()
    x = x + 1
for line in input:      #reads counts and converts to energy
    energy = float(line) * 0.0266 + 0.133
    output.write(str(energy))
    output.write('\n')

# energy in keV = counts * slope + offset
# slope = 0.0266
# offset = 0.113
