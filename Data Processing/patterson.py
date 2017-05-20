#!/usr/bin/python
import numpy as np
import numpy.linalg as npl
import math
import cmath
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



#---------------------define the constants------------------------------
energy = 10.0
density = 9.45 #density of TiO2 Rutile , water is 9.45
pmax = 100 #patterson function, maximal value.

K0 = energy*1000/1973.0
waveleng = 2*math.pi/K0
qc = 4*math.sqrt(math.pi*density*1.0E-6)

print 'Critical wave vector is:', qc, ' (1/Angstrom)'
#------------------end of defining the constants----------------------

#plot the figure;
def plotFigures(q, xx, patt, rrf, drrf):
  plt.figure(figsize=(11,8.5))
  plt.suptitle('$Scan$#:$'+ scanNumber + '$\n' + scanComment)
  plt.subplot(212)
  plt.plot(xx, patt, 'b', linewidth = 2.5)
  plt.ylabel('Patterson')
  plt.xlabel('$x$ ($\AA$)')
  plt.grid(color='g', linestyle=':', linewidth = 0.8)
  figure1 = plt.gca()
  plt.xlim(0,1.02*max(xx))
  
  plt.subplot(211)
  plt.errorbar(q, rrf , yerr = drrf, fmt = 'r.', ecolor = 'b', linewidth = 0.5)
  plt.xlabel('$q$ ($\AA$$^{-1}$)')
  plt.ylabel('$R/R_F$')
  plt.xlim(0,1.02*max(q))
  plt.grid(color = 'g', linestyle=':', linewidth = 0.8)
  figure2 = plt.gca()
  figure2.set_yscale('log')
  
  pp = plt.gcf()
  pp = PdfPages(scanNumber + '.pdf')
  pp.savefig()
  pp.close()
  plt.show()

def saveData(q, r, dr):
  datafile = open(scanNumber + '.txt','w')
  temp = r[0]
  for n in range(len(q)):
    datafile.write('%.4f\t%.4e\t%.4e\t%f\n' %(q[n], r[n]/temp, dr[n]/temp, count[n]*temp))
#------------------------------------------------------------------------------------

def readFile(fileName): #read the file and convert it to q, r, dr. 
  with open(fileName) as f:
    content = []
    for line in f:
      content.append([x if 'T' in x or 'x' in x else float(x) for x in line.split()])
    q = []; r = []; dr = []
    for n in range(len(content)):
      q.append(content[n][0])
      r.append(content[n][1])
      dr.append(content[n][2])
  return q, r, dr


def r2rf(q, r, dr):
  if len(q) != len(r):
    print 'Check dimension!'
    sys.exit()
  rf = []; drf = []; rrf = []
  for n in range(len(q)):
    if q[n] <= qc:
      rf.append(1)
    else:
      rf.append(((q[n] - math.sqrt(q[n]**2 - qc**2))/(q[n] + math.sqrt(q[n]**2 - qc**2)))**2)
  for n in range(len(q)):
    rrf.append(r[n]/rf[n])
    drf.append(dr[n]/rf[n])
  return rrf, drf

def patterson(q, r, dr):
  if len(q) < 20:
    print 'Too few data points'
    patt = []
    return patt
  rrf, drf = r2rf(q, r, dr)
  qpa = [0 for n in range(2*len(q))]
  rpa = [0 for n in range(2*len(q))]
  for n in range(2*len(q)):
    if n < len(q):
      qpa[n] = q[n]
      rpa[n] = rrf[n]
    else:
      qpa[n] = q[-1] + (q[-1] - q[-2])*( n - len(q) + 1)
      rpa[n] = rrf[-1]*math.exp(-(qpa[n])**2/0.6)*math.exp(q[-1]**2/0.6)
  
  xx = np.linspace(0, pmax, 200)
  patt = [0 for n in range(200)]
  for n in range(len(xx)):
    patt[n] = 0
    for m in range(1, 2*len(q)):
      dq = qpa[m] - qpa[m - 1]
      patt[n] += rpa[m]*math.cos(qpa[m]*xx[n])*dq

  return xx, patt

#-------------------here begins the main script--------------------------------------

if len(sys.argv) not in [2]:
  print 'python patterson.py data.txt'
  sys.exit() 

fname  =  sys.argv[1]
fNumber = 1


scanNumber = fname 
scanComment = ('Patterson Function')

q = []; r = []; dr = []

q, r, dr = readFile(fname)
rrf, drrf = r2rf(q, r, dr)
xx, patt = patterson(q, r, dr)
plotFigures(q, xx, patt, rrf, drrf)
