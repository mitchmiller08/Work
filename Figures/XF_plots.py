import numpy as np
import matplotlib.pyplot as plt
from operator import add

#Set x values
erx = [5e-8,1e-7,5e-7,1e-6,5e-6,1e-5,1e-4]
ndx = [1e-7,5e-7,1e-6,1e-5,1e-4]
mixx = [0,5e-5,5.5e-5,6e-5,7.55e-5]

#set y values
ery = [0.001,0.016,0.015,0.016,0.015,0.018,0.014]
ndy = [0.000,0.000,0.015,0.013,0.012]
mixery = [0,0.011,0.012,0.014,0.015]
mixndy = [0.012,0.005,0.005,0.005,0.003]
mixsumy = map(add, mixery,mixndy)

#set sdv values
ersdv = [2.64e-4,3.16e-4,3.28e-4,5.36e-4,2.05e-4,3.58e-4,1.84e-4]
ndsdv = [0.001,6.02e-5,3.54e-4,3.13e-4,2.01e-4]
mixersdv = [0,2.08e-4,3.14e-4,3.49e-4,3.41e-4]
mixndsdv = [2.01e-4,1.26e-4,1.82e-4,1.83e-4,1.21e-4]
mixsumsdv = map(add, mixersdv,mixndsdv)

#create figures
plt.figure(1)
plt.xscale('log')
plt.xlim([1e-8,5e-4])
plt.ylim([0,0.02])
plt.xlabel('Concentration (M)')
plt.ylabel(r'Surface Density $(\AA^{-2})$')
plt.errorbar(erx,ery,yerr=ersdv,linestyle="None",elinewidth=2,capthick=2)
#plt.show()
plt.savefig('Er_XF.png',dpi=500)

plt.figure(2)
plt.xscale('log')
plt.xlim([5e-8,5e-4])
plt.ylim([-0.002,0.002])
plt.yticks(np.arange(0,0.021,0.005))
plt.xlabel('Concentration (M)')
plt.ylabel(r'Surface Density $(\AA^{-2})$')
plt.errorbar(ndx,ndy,yerr=ndsdv,linestyle="None",elinewidth=2,capthick=2)
#plt.show()
plt.savefig('Nd_XF.png',dpi=500)

plt.figure(3)
plt.xlim([4e-5,8e-5])
plt.ylim([0,0.022])
plt.yticks(np.arange(0,0.021,0.005))
plt.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
plt.xlabel('Concentration (M)')
plt.ylabel(r'Surface Density $(\AA^{-2})$')
plt.errorbar(mixx,mixery,yerr=mixersdv,linestyle="None",label="Erbium",elinewidth=2,capthick=2)
plt.errorbar(mixx,mixndy,yerr=mixndsdv,linestyle="None",label="Neodymium",elinewidth=2,capthick=2)
plt.errorbar(mixx,mixsumy,yerr=mixsumsdv,linestyle="None",label="Sum",elinewidth=2,capthick=2)
plt.legend(loc=2,numpoints=1)
#plt.show()
plt.savefig('Sum_XF.png',dpi=500)