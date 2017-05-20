import numpy as np
import matplotlib.pyplot as plt


def importdata3col(filename):
	data = np.genfromtxt(filename,delimiter='\t')
	x = data[:,0]
	y = data[:,1]
	yerr = data[:,2]
	return x,y,yerr
	
def importdata4col(filename):
	#Read data
	data = np.genfromtxt(filename,delimiter='\t')
	x = data[:,0]
	y = data[:,1]
	z = data[:,2]
	#Reshape arrays
	x=np.unique(x)
	y=np.unique(y)
	X,Y = np.meshgrid(x,y)
	Z = z.reshape(len(y),len(x))
	return X,Y,Z
	
def backgroundsubtract(peak,peakerr,back1,back1err,back2,back2err):
	noback = peak - 0.5*(back1 + back2)
	nobackerr = np.sqrt(peakerr**2 + back1err**2 + back2err**2)
	return noback, nobackerr
	
def normalizedata(y,error):

	max = y.max()
	y = y / max
	error = error / max
	return y, error
	
	
##Import tab delimiter 3 column file
#Qxy data
x_xy, y_xy, yerr_xy = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Er_412-417_qxy_gid.txt')
y_xy = y_xy - y_xy.min() + 50											#Subtract flat background amount

#Rod scan data
x_rod1, y_rod1, yerr_rod1 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_072-076.txt')
x_rod1b1, y_rod1b1, yerr_rod1b1 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_056-060_back.txt')
x_rod1b2, y_rod1b2, yerr_rod1b2 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_078-082_back.txt')

x_rod2, y_rod2, yerr_rod2 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_118-122.txt')
x_rod2b1, y_rod2b1, yerr_rod2b1 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_113-117_back.txt')
x_rod2b2, y_rod2b2, yerr_rod2b2 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_123-127_back.txt')

x_rod3, y_rod3, yerr_rod3 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_145-155.txt')
x_rod3b1, y_rod3b1, yerr_rod3b1 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_100-110_back.txt')
x_rod3b2, y_rod3b2, yerr_rod3b2 = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qz\Er_411-412\Er_411-417_155-165_back.txt')

#Remove background
y_rod1noback, yerr_rod1noback = backgroundsubtract(y_rod1,yerr_rod1,y_rod1b1,yerr_rod1b1,y_rod1b2,yerr_rod1b2)
y_rod2noback, yerr_rod2noback = backgroundsubtract(y_rod2,yerr_rod2,y_rod2b1,yerr_rod2b1,y_rod2b2,yerr_rod2b2)
y_rod3noback, yerr_rod3noback = backgroundsubtract(y_rod3,yerr_rod3,y_rod3b1,yerr_rod3b1,y_rod3b2,yerr_rod3b2)


##Import tab delimiter 4 column file
#2D Data
x_2d, y_2d, z_2d = importdata4col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Q2d\Er_test_411-417.txt')

#Normalize data
y_xy, yerr_xy = normalizedata(y_xy, yerr_xy)
y_rod1noback, yerr_rod1noback = normalizedata(y_rod1noback, yerr_rod1noback)
y_rod2noback, yerr_rod2noback = normalizedata(y_rod2noback, yerr_rod2noback)
y_rod3noback, yerr_rod3noback = normalizedata(y_rod3noback, yerr_rod3noback)

##Set layout of grid - 2 panel in left column, 3 panel in right
ax2 = plt.subplot2grid((6,3),(3,0),rowspan=3,colspan=2)
ax1 = plt.subplot2grid((6,3),(0,0),rowspan=3,colspan=2)
ax5 = plt.subplot2grid((6,3),(4,2),rowspan=2)
ax3 = plt.subplot2grid((6,3),(0,2),rowspan=2)
ax4 = plt.subplot2grid((6,3),(2,2),rowspan=2)

plt.subplots_adjust(wspace=0.5)											#Set horizontal spacing
plt.subplots_adjust(hspace=0.5)											#Set vertical spacing

##Add labels and indices
#Labels
ax1.set_ylabel(r'$Q_{z} (\AA^{-1})$')

ax2.set_xlabel(r'$Q_{xy} (\AA^{-1})$')
ax2.set_ylabel('Intensity (arb. units)')

ax4.set_ylabel('Intensity (arb.units)')
ax5.set_xlabel(r'$Q_{z} (\AA^{-1})$')

ax1.text(0.54,0.6,'(a)',bbox=dict(boxstyle='round',fc='white'))
ax2.text(0.54,1.1,'(b)')
ax3.text(0.55,0.8,'(c)')
ax4.text(0.55,0.8,'(d)')
ax5.text(0.55,0.8,'(e)')

#Indices
ax2.text(0.6,0.35,r'$(\frac{1}{2}0)C$',rotation='vertical')
ax2.text(0.69,1.075,r'$(\frac{1}{2}\frac{1}{2})C$',rotation='vertical')
ax2.text(0.91,0.3,r'$(10)I$',rotation='vertical')
ax2.text(1.16,1.0,r'$(01)I$',rotation='vertical')
ax2.annotate(r'$(10)M$',rotation='vertical',xy=(1.32,0.3),xytext=(1.25,0.6),arrowprops=dict(arrowstyle='->'))
ax2.text(1.33,0.9,r'$(01)M$',rotation='vertical')
ax2.text(1.44,1.2,r'$(11)M$',rotation='vertical')
ax2.text(1.62,0.6,r'$(1\overline{1})I$',rotation='vertical')
ax2.text(1.755,0.65,r'$(\frac{3}{2}\frac{1}{2})C$',rotation='vertical')
ax2.text(1.84,0.9,r'$(\frac{1}{2}\frac{3}{2})C$',rotation='vertical')
ax2.text(1.84,1.14,r'$(20)I$',rotation='vertical')
ax2.text(1.955,0.75,r'$(\frac{3}{2}0)C$',rotation='vertical')


##Do plots
#2D Plot
ax1.contourf(x_2d,y_2d,z_2d,cmap=plt.get_cmap('jet'),levels=np.arange(0,z_2d.max(),10))
ax1.set_xlim([max(x_2d.min(),x_xy.min()),min(x_2d.max(),x_xy.max())])   #Ensure x range is same for 2d and xy plots
ax1.set_ylim([0,y_2d.max()])											#Cut below plane
plt.setp(ax1.get_xticklabels(),visible=False)							#Hide tick labels

#Qxy plot
ptsize=2
linew=0.5

ax2.plot(x_xy,y_xy,marker='.',markersize=ptsize,linewidth=linew)

ax2.set_xlim([max(x_2d.min(),x_xy.min()),min(x_2d.max(),x_xy.max())])	#Ensure x range is same for 2d and xy plots
ax2.set_ylim([0,1.3*y_xy.max()])

ax2.set_xticks(np.arange(0.5,2.5,0.1),minor=True)
ax2.set_yticks(np.arange(0,1.4,0.2))

#Rod scans
ax3.plot(x_rod1,y_rod1noback,marker='.',markersize=ptsize,linewidth=linew)
plt.setp(ax3.get_xticklabels(),visible=False)							#Hide tick labels
ax4.plot(x_rod2,y_rod2noback,marker='.',markersize=ptsize,linewidth=linew)
plt.setp(ax4.get_xticklabels(),visible=False)							#Hide tick labels
ax5.plot(x_rod3,y_rod3noback,marker='.',markersize=ptsize,linewidth=linew)

ax3.set_ylim([-0.1,1.1])
ax4.set_ylim([-0.1,1.1])
ax5.set_ylim([-0.1,1.1])

major_ticks = np.arange(0,0.8,0.2)										#Set major tick spacing
minor_ticks = np.arange(0,0.8,0.1)										#Set minor tick spacing

ax3.set_xticks(major_ticks)
ax3.set_xticks(minor_ticks,minor=True)
ax4.set_xticks(major_ticks)
ax4.set_xticks(minor_ticks,minor=True)
ax5.set_xticks(major_ticks)
ax5.set_xticks(minor_ticks,minor=True)
ax3.set_yticks(np.arange(0,1.1,0.2))
ax4.set_yticks(np.arange(0,1.1,0.2))
ax5.set_yticks(np.arange(0,1.1,0.2))



##Save plot
plt.savefig('ODP_Er_survey.png',dpi=500)
plt.show()



