import numpy as np
import matplotlib.pyplot as plt


def importdata3col(filename):
	data = np.genfromtxt(filename,delimiter="\t")
	x = data[:,0]
	y = data[:,1]
	yerr = data[:,2]
	return x,y,yerr
	
def importc21(prefix,appendix,scannumbers):

	pathlist = []
	xlist = []
	ylist = []
	yerrlist = []
	
	for num in scannumbers:
		pathlist.append(prefix+str(num)+appendix)
	
	for path in pathlist:
		x,y,yerr = importdata3col(path)
		xlist.append(x)
		ylist.append(y)
		yerrlist.append(yerr)
	
	return xlist,ylist,yerrlist

def stripdata(min,max,x,y,yerr):
	
	i=0
	while i < len(x):
		if x[i] < min or x[i] > max:
			x = np.delete(x,i,None)
			y = np.delete(y,i,None)
			yerr = np.delete(yerr,i,None)
		else:
			i = i + 1
			
	return x, y, yerr
	
def normalizedata(y,error):

	max = y.max()
	y = y / max
	error = error / max
	return y, error
	
def normalizec21data(y,error):

	max = 0
	for row in y:
		if row.max() > max:
			max = row.max()
	
	i=0
	for row in y:
		y[i] = y[i] / max
		i += 1
	
	i=0
	for row in error:
		error[i] = error[i] / max
		i += 1
	
	return y, error

##Import data	
x_odpl, y_odpl, yerr_odpl = importdata3col(r"E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Nd_420-426_qxy_gid.txt")
x_odph, y_odph, yerr_odph = importdata3col(r"E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Er_412-417_qxy_gid.txt")
x_dhdph, y_dhdph, yerr_dhdph = importdata3col(r"E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Er_541-548_qxy_gid.txt")
x_dhdpl, y_dhdpl, yerr_dhdpl = importdata3col(r"E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Nd_45-52_qxy_gid.txt")

#C21 light
ndscans = range(141,149+1,1)
ndx,ndy,ndyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Nd_141-149\QxyProfiles\Backup\Nd_C21_S# ','_F# 0_cut.txt',ndscans)
del ndx[4],ndy[4],ndyerr[4]

#C21 heavy
erscans = range(21,28+1,1)
erx,ery,eryerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Er_C21_21-28\Er_C21_S# ','_F# 0_cut.txt',erscans)

#Strip C21 data
erx[0],ery[0],eryerr[0] = stripdata(0.515,0.60,erx[0],ery[0],eryerr[0])
erx[1],ery[1],eryerr[1] = stripdata(0.82,0.9,erx[1],ery[1],eryerr[1])
erx[2],ery[2],eryerr[2] = stripdata(1.025,1.12,erx[2],ery[2],eryerr[2])
erx[3],ery[3],eryerr[3] = stripdata(1.24,1.355,erx[3],ery[3],eryerr[3])
erx[4],ery[4],eryerr[4] = stripdata(1.35,1.54,erx[4],ery[4],eryerr[4])
erx[5],ery[5],eryerr[5] = stripdata(1.55,1.8,erx[5],ery[5],eryerr[5])
erx[6],ery[6],eryerr[6] = stripdata(1.81,1.86,erx[6],ery[6],eryerr[6])
#erx[7],ery[7],eryerr[7] = stripdata(2.15,1.86,erx[7],ery[7],eryerr[7])
del erx[7],ery[7],eryerr[7]

ndx[0],ndy[0],ndyerr[0] = stripdata(0.494,0.60,ndx[0],ndy[0],ndyerr[0])
ndx[1],ndy[1],ndyerr[1] = stripdata(0.8,0.98,ndx[1],ndy[1],ndyerr[1])
ndx[2],ndy[2],ndyerr[2] = stripdata(1.0,1.21,ndx[2],ndy[2],ndyerr[2])
ndx[3],ndy[3],ndyerr[3] = stripdata(1.22,1.4,ndx[3],ndy[3],ndyerr[3])
ndx[4],ndy[4],ndyerr[4] = stripdata(1.39,1.59,ndx[4],ndy[4],ndyerr[4])
ndx[5],ndy[5],ndyerr[5] = stripdata(1.58,1.79,ndx[5],ndy[5],ndyerr[5])
ndx[6],ndy[6],ndyerr[6] = stripdata(1.77,1.86,ndx[6],ndy[6],ndyerr[6])
#ndx[7],ndy[7],ndyerr[7] = stripdata(2.1,1.86,ndx[7],ndy[7],ndyerr[7])
del ndx[7],ndy[7],ndyerr[7]

#Normalize data
y_odpl, yerr_odpl = normalizedata(y_odpl, yerr_odpl)
y_odph, yerr_odph = normalizedata(y_odph, yerr_odph)
y_dhdph, yerr_dhdph = normalizedata(y_dhdph, yerr_dhdph)
y_dhdpl, yerr_dhdpl = normalizedata(y_dhdpl, yerr_dhdpl)
ery,eryerr = normalizec21data(ery,eryerr)
ndy,ndyerr = normalizec21data(ndy,ndyerr)

#Subtract flat background
y_odpl = y_odpl - y_odpl.min() + 0.05
y_odph = y_odph - y_odph.min() + 0.05
y_dhdpl = y_dhdpl - y_dhdpl.min() + 0.05
y_dhdph = y_dhdph - y_dhdph.min() + 0.05


##Set layout
ax1 = plt.subplot2grid((6,1),(0,0))
ax2 = plt.subplot2grid((6,1),(1,0))
ax3 = plt.subplot2grid((6,1),(2,0))
ax4 = plt.subplot2grid((6,1),(3,0))
ax5 = plt.subplot2grid((6,1),(4,0))
ax6 = plt.subplot2grid((6,1),(5,0))

#Set x tickmarks
ax1.set_xticks(np.arange(0.2,2.5,0.2))
ax2.set_xticks(np.arange(0.2,2.5,0.2))
ax3.set_xticks(np.arange(0.2,2.5,0.2))
ax4.set_xticks(np.arange(0.2,2.5,0.2))
ax5.set_xticks(np.arange(0.2,2.5,0.2))
ax6.set_xticks(np.arange(0.2,2.5,0.2))
ax1.set_xticks(np.arange(0.2,2.5,0.05),minor=True)
ax2.set_xticks(np.arange(0.2,2.5,0.05),minor=True)
ax3.set_xticks(np.arange(0.2,2.5,0.05),minor=True)
ax4.set_xticks(np.arange(0.2,2.5,0.05),minor=True)
ax5.set_xticks(np.arange(0.2,2.5,0.05),minor=True)
ax6.set_xticks(np.arange(0.2,2.5,0.05),minor=True)

#Set x range
odplmin = x_odpl.min()
odplmax = x_odpl.max()
odphmin = x_odph.min()
odphmax = x_odph.max()
dhdplmin = x_dhdpl.min()
dhdplmax = x_dhdpl.max()
dhdphmin = x_dhdph.min()
dhdphmax = x_dhdph.max()
#c21lmin = x_c21l_1.min()
#c21lmax = x_c21l_7.max()

rangemin = max(odplmin,dhdplmin,dhdphmin)
rangemax = min(odplmax,dhdplmax,dhdphmax)

ax1.set_xlim([rangemin,rangemax])
ax2.set_xlim([rangemin,rangemax])
ax3.set_xlim([rangemin,rangemax])
ax4.set_xlim([rangemin,rangemax])
ax5.set_xlim([rangemin,rangemax])
ax6.set_xlim([rangemin,rangemax])

#Set y range
ax1.set_ylim([0,1.1])
ax2.set_ylim([0,1.3])
ax3.set_ylim([0,1.1])
ax4.set_ylim([0,1.1])
ax5.set_ylim([0,1.1])
ax6.set_ylim([0,1.1])

#Set y tickmarks
ax1.set_yticks(np.arange(0,1.1,0.2))
ax2.set_yticks(np.arange(0,1.1,0.2))
ax3.set_yticks(np.arange(0,1.1,0.2))
ax4.set_yticks(np.arange(0,1.1,0.2))
ax5.set_yticks(np.arange(0,1.1,0.2))
ax6.set_yticks(np.arange(0,1.1,0.2))

#Set tick labels font size
ax1.tick_params(axis='both', which='major', labelsize=10)
ax2.tick_params(axis='both', which='major', labelsize=9)
ax3.tick_params(axis='both', which='major', labelsize=10)
ax4.tick_params(axis='both', which='major', labelsize=10)
ax5.tick_params(axis='both', which='major', labelsize=10)
ax6.tick_params(axis='both', which='major', labelsize=10)

#Hide tick labels
plt.setp(ax1.get_xticklabels(),visible=False)
plt.setp(ax2.get_xticklabels(),visible=False)
plt.setp(ax3.get_xticklabels(),visible=False)
plt.setp(ax4.get_xticklabels(),visible=False)
plt.setp(ax5.get_xticklabels(),visible=False)

#Set axis labels
ax6.set_xlabel(r'$Q_{xy} (\AA^{-1})$')
ax3.text(0.0,0.8,'Intensity (arb.units)',rotation='vertical')

#Add panel labels
ax1.text(2.1,0.7,'ODPA Nd')
ax1.text(0.3,0.7,'(a)')
ax2.text(2.1,0.7, 'ODPA Er')
ax2.text(0.3,0.7,'(b)')
ax3.text(2.1,0.7,'HIA Nd')
ax3.text(0.3,0.7,'(c)')
ax4.text(2.1,0.7,'HIA Er')
ax4.text(0.3,0.7,'(d)')
ax5.text(2.1,0.7,'DHDP Nd')
ax5.text(0.3,0.7,'(e)')
ax6.text(2.1,0.7,'DHDP Er')
ax6.text(0.3,0.7,'(f)')

##Add indices
#ODP Light
ax1.text(0.39,0.75,r'$(10)C$',rotation='vertical')
ax1.text(1.35,0.75,r'$(10)M$',rotation='vertical')
ax1.text(1.55,0.85,r'$(11)M$',rotation='vertical')

#ODP Heavy
ax2.text(0.65,0.7,r'$(\frac{1}{2}0)C$',rotation='vertical')
ax2.text(0.76,0.85,r'$(\frac{1}{2}\frac{1}{2})C$',rotation='vertical')
ax2.text(0.91,0.65,r'$(10)I$',rotation='vertical')
ax2.annotate(r'$(10)M$',rotation='vertical',xy=(1.32,0.3),xytext=(1.25,0.9),arrowprops=dict(arrowstyle='->'))
ax2.annotate(r'$(01)I$',rotation='vertical',xy=(1.2,0.6),xytext=(1.1,0.9),arrowprops=dict(arrowstyle='->'))
ax2.annotate(r'$(01)M$',rotation='vertical',xy=(1.36,0.6),xytext=(1.4,0.9),arrowprops=dict(arrowstyle='->'))
ax2.annotate(r'$(11)M$',rotation='vertical',xy=(1.48,0.83),xytext=(1.52,1.0),arrowprops=dict(arrowstyle='->'))
ax2.text(1.62,0.9,r'$(1\overline{1})I$',rotation='vertical')
ax2.text(1.755,0.95,r'$(\frac{3}{2}\frac{1}{2})C$',rotation='vertical')
#ax2.text(1.84,0.9,r'$(\frac{1}{2}\frac{3}{2})C$',rotation='vertical',size=8)
#ax2.text(1.84,1.14,r'$(20)I$',rotation='vertical',size=8)
ax2.text(1.955,0.95,r'$(\frac{3}{2}0)C$',rotation='vertical')
ax2.annotate(r'$(\frac{1}{2}\frac{3}{2})C$'+'\n$(20)I$',rotation='vertical',xy=(1.88,0.6),xytext=(1.85,0.75),fontsize=7,arrowprops=dict(arrowstyle='->'),bbox=dict(boxstyle='round',fc='white'))

#DHDP Light
ax5.text(1.56,0.8,r'$(11)M$',rotation='vertical')

#DHDP Heavy
ax6.text(0.56,0.6,r'$(10)I$',rotation='vertical')
ax6.text(1.34,0.85,r'$(10)M$',rotation='vertical')
ax6.annotate(r'$(11)M$',rotation='vertical',xy=(1.57,0.45),xytext=(1.67,0.85),arrowprops=dict(arrowstyle='->'))

#C21 Heavy
ax4.text(0.575,0.6,r'$(10)I$',rotation='vertical')
ax4.text(0.82,0.65,r'$(\frac{1}{2}\frac{1}{2})C$',rotation='vertical')
ax4.text(1.045,0.65,r'$(02)I$',rotation='vertical')
ax4.text(1.2,0.55,r'$(\frac{1}{2}\overline{\frac{1}{2}})C$',rotation='vertical')
ax4.text(1.31,0.8,r'$(10)M$',rotation='vertical')
ax4.annotate(r'$(01)M$',rotation='vertical',xy=(1.6,0.5),xytext=(1.51,0.75),arrowprops=dict(arrowstyle='->'))
ax4.text(1.66,0.8,r'$(11)M$',rotation='vertical')

#C21 Light
ax3.text(0.54,0.5,r'$(01)I$',rotation='vertical')
ax3.text(0.87,0.5,r'$(21)I$',rotation='vertical')
ax3.annotate(r'$(02)I$',rotation='vertical',xy=(1.01,0.07),xytext=(0.95,0.75),arrowprops=dict(arrowstyle='->'))
ax3.annotate(r'$(20)I$',rotation='vertical',xy=(1.03,0.07),xytext=(1.02,0.75),arrowprops=dict(arrowstyle='->'))
ax3.annotate(r'$(13)I$',rotation='vertical',xy=(1.35,0.12),xytext=(1.28,0.75),arrowprops=dict(arrowstyle='->'))
ax3.annotate(r'$(31)I$',rotation='vertical',xy=(1.38,0.12),xytext=(1.35,0.75),arrowprops=dict(arrowstyle='->'))
ax3.text(1.41,0.9,r'$(10)M$',rotation='vertical')
ax3.text(1.54,0.7,r'$(30)I$',rotation='vertical')
ax3.text(1.655,0.7,r'$(11)M$',rotation='vertical')
ax3.annotate(r'$(2\overline{2})I$',rotation='vertical',xy=(1.755,0.1),xytext=(1.73,0.7),arrowprops=dict(arrowstyle='->'))
ax3.annotate(r'$(42)I$',rotation='vertical',xy=(1.8,0.15),xytext=(1.82,0.7),arrowprops=dict(arrowstyle='->'))
ax3.annotate('$(01)M$\n$(03)I$',rotation='vertical',xy=(1.53,0.95),xytext=(1.92,0.35),arrowprops=dict(arrowstyle='->',connectionstyle="angle,angleA=90,angleB=0,rad=10"),bbox=dict(boxstyle='round',fc='white'))


##Do plots
ptsize=2
linew=0.5
#ax1.errorbar(x_odpl,y_odpl,yerr=yerr_odpl)
ax1.plot(x_odpl,y_odpl,marker='.',markersize=ptsize,linewidth=linew)

#ax2.errorbar(x_dhdpl,y_dhdpl,yerr=yerr_dhdpl)
ax2.plot(x_odph,y_odph,marker='.',markersize=ptsize,linewidth=linew)

#ax3.errorbar(x_dhdph,y_dhdph,yerr=yerr_dhdph)
ax6.errorbar(x_dhdph,y_dhdph,marker='.',markersize=ptsize,linewidth=linew)

ax5.errorbar(x_dhdpl,y_dhdpl,marker='.',markersize=ptsize,linewidth=linew)

i = 0
while i < len(erx):
	ax4.plot(erx[i],ery[i],marker='.',color='blue',markersize=ptsize,linewidth=linew)
	i = i + 1

i = 0
while i < len(ndx):
	ax3.plot(ndx[i],ndy[i],marker='.',color='blue',markersize=ptsize,linewidth=linew)
	i = i + 1


plt.savefig('Qxy_summary.png',dpi=500)
plt.show()