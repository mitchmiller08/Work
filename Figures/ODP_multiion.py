import numpy as np
import matplotlib.pyplot as plt


def importdata3col(filename):
	data = np.genfromtxt(filename,delimiter="\t")
	x = data[:,0]
	y = data[:,1]
	yerr = data[:,2]
	return x,y,yerr

def backgroundsubtract(y):
	y = y - y.min() + 50
	return y
	
def normalizedata(y,error,stacks):

	max = y.max()
	y = y / (max*stacks)
	error = error / (max*stacks)
	return y, error
	
##Import data
#Heavy
ybx,yby,ybyerr = importdata3col('E:\APS Data\Sector 15\Nov14 Data\extracted_data\Qxy\Yb_121-127_qxy_gid.txt')
erx,ery,eryerr = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Er_412-417_qxy_gid.txt')
dyx,dyy,dyyerr = importdata3col('E:\APS Data\Sector 15\Nov14 Data\extracted_data\Qxy\Dy_147-153_qxy_gid.txt')
#Light
cex,cey,ceyerr = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Ce_456-462_qxy_gid.txt')
ndx,ndy,ndyerr = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Nd_420-426_qxy_gid.txt')
prx,pry,pryerr = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Pr_498-504_qxy_gid.txt')
smx,smy,smyerr = importdata3col('E:\APS Data\Sector 15\Feb16 Data\extracted_data\Qxy\Sm_438-444_qxy_gid.txt')

#Subtract flat background amount
yby = backgroundsubtract(yby)
ery = backgroundsubtract(ery)
dyy = backgroundsubtract(dyy)

ndy = backgroundsubtract(ndy)
pry = backgroundsubtract(pry)
cey = backgroundsubtract(cey)
smy = backgroundsubtract(smy)

#Normalize data
yby,ybyerr = normalizedata(yby,ybyerr,3)
ery,eryerr = normalizedata(ery,eryerr,3)
dyy,dyyerr = normalizedata(dyy,dyyerr,3)

ndy,ndyerr = normalizedata(ndy,ndyerr,1)
pry,pryerr = normalizedata(pry,pryerr,1)
cey,ceyerr = normalizedata(cey,ceyerr,1)
smy,smyerr = normalizedata(smy,smyerr,1)

##Set layout
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))

#Set tickmarks
ax1.set_xticks(np.arange(0.2,2.5,0.2))
ax2.set_xticks(np.arange(0.2,2.5,0.2))
ax1.set_xticks(np.arange(0.2,2.5,0.05),minor=True)
ax2.set_xticks(np.arange(0.2,2.5,0.05),minor=True)

#Set x range
rangemin = min(ybx.min(),erx.min(),dyx.min(),ndx.min(),prx.min(),cex.min(),smx.min())
rangemax = min(ybx.max(),erx.max(),dyx.max(),ndx.max(),prx.max(),cex.max(),smx.max())

ax1.set_xlim([rangemin,rangemax])
ax2.set_xlim([rangemin,rangemax])

#Set y range
heightmaxh = max(yby.max(),ery.max(),dyy.max())
heightmaxl = max(cey.max(),ndy.max(),pry.max(),smy.max())
ax1.set_ylim([0,1.1])
ax2.set_ylim([0,1.1])

#Hide tick labels for upper plot
plt.setp(ax1.get_xticklabels(),visible=False)

#Set axis labels
ax2.set_xlabel(r'$Q_{xy} (\AA^{-1})$')
ax1.text(0,0.05,'Intensity (arb.units)',rotation='vertical')

#Add peak lines
ax1.axvline(x=0.672,color='black',linewidth=0.2)
ax1.axvline(x=0.742,color='black',linewidth=0.2)
ax1.axvline(x=0.951,color='black',linewidth=0.2)
ax1.axvline(x=1.208,color='black',linewidth=0.2)
ax1.axvline(x=1.340,color='black',linewidth=0.2)
ax1.axvline(x=1.362,color='black',linewidth=0.2)
ax1.axvline(x=1.490,color='black',linewidth=0.2)
ax1.axvline(x=1.667,color='black',linewidth=0.2)
ax1.axvline(x=1.803,color='black',linewidth=0.2)
ax1.axvline(x=1.887,color='black',linewidth=0.2)
ax1.axvline(x=2.010,color='black',linewidth=0.2)

#Add ion labels
ax1.text(2.3,0.3/3+0.05,'Er')
ax1.text(2.3,1.4/3,'Dy')
ax1.text(2.3,2.3/3,'Yb')

#Add panel labels
ax1.text(0.32,1.0,'(a)')
ax2.text(0.32,1.0,'(b)')

#Add indices
plt.figtext(0.255,0.95,r'$(\frac{1}{2}0)C$',rotation='vertical')
plt.figtext(0.285,0.95,r'$(\frac{1}{2}\frac{1}{2})C$',rotation='vertical')
plt.figtext(0.36,0.95,r'$(10)I$',rotation='vertical')
plt.figtext(0.46,0.95,r'$(01)I$',rotation='vertical')
plt.figtext(0.5,0.95,r'$(10)M$',rotation='vertical',fontsize=10)
plt.figtext(0.52,0.95,r'$(01)M$',rotation='vertical',fontsize=10)
plt.figtext(0.56,0.95,r'$(11)M$',rotation='vertical',fontsize=10)
plt.figtext(0.62,0.95,r'$(1\overline{1})I$',rotation='vertical')
plt.figtext(0.67,0.95,r'$(\frac{3}{2}\frac{1}{2})C$',rotation='vertical')
plt.figtext(0.75,0.95,r'$(\frac{3}{2}0)C$',rotation='vertical')
ax1.annotate("$(\\frac{1}{2}\\frac{3}{2})C$\n$(20)I$",rotation='vertical',xy=(1.88,1.05),xytext=(2.2,1.15),arrowprops=dict(arrowstyle='->',connectionstyle="angle,angleA=90,angleB=0,rad=10"),bbox=dict(boxstyle='round',fc='white'))

ax2.text(0.39,0.5,r'$(10)C$',rotation='vertical')
ax2.text(1.35,0.7,r'$(10)M$',rotation='vertical')
ax2.text(1.55,0.7,r'$(11)M$',rotation='vertical')

##Do plots
ptsize=2
linew=0.5

ax1.plot(erx,ery,marker='.',markersize=ptsize,linewidth=linew)
ax1.plot(dyx,dyy+1/3.,marker='.',markersize=ptsize,linewidth=linew)
ax1.plot(ybx,yby+2/3.,marker='.',markersize=ptsize,linewidth=linew)

ax2.plot(cex,cey,marker='.',markersize=ptsize,linewidth=linew, label='Ce')
ax2.plot(prx,pry,marker='.',markersize=ptsize,linewidth=linew, label='Pr')
ax2.plot(ndx,ndy,marker='.',markersize=ptsize,linewidth=linew, label='Nd')
ax2.plot(smx,smy,marker='.',markersize=ptsize,linewidth=linew, label='Sm')
ax2.legend(loc=1,prop={'size':12})

plt.savefig('ODP_multiion.pdf',dpi=500)
plt.show()