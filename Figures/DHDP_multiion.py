import numpy as np
import matplotlib.pyplot as plt


def importdata3col(filename):
	data = np.genfromtxt(filename,delimiter="\t")
	x = data[:,0]
	y = data[:,1]
	yerr = data[:,2]
	return x,y,yerr

def backgroundsubtract(y):
	y = y - y.min() + 200
	return y
	
def normalizedata(y,error):

	max = y.max()
	y = y / max
	error = error / max
	return y, error

##Import data
#Heavy
ybx,yby,ybyerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Yb_71-78_qxy_gid.txt')
erx,ery,eryerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Er_541-548_qxy_gid.txt')
dyx,dyy,dyyerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Dy_6-13_qxy_gid.txt')
tbx,tby,tbyerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Tb_435-444_qxy_gid.txt')

#Light
lax,lay,layerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\La_32-39_qxy_gid.txt')
ndx,ndy,ndyerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Nd_45-52_qxy_gid.txt')
eux,euy,euyerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Eu_58-65_qxy_gid.txt')
gdx,gdy,gdyerr = importdata3col('E:\APS Data\Sector 15\July14 Data\extracted_data\Qxy\Gd_569-576_qxy_gid.txt')

cex,cey,ceyerr = importdata3col(r'E:\APS Data\Sector 15\Oct15 Data\2015oct\extracted_data\Qxy\Ce_798-803_qxy_gid.txt')
prx,pry,pryerr = importdata3col(r'E:\APS Data\Sector 15\Oct15 Data\2015oct\extracted_data\Qxy\Pr_790-795_qxy_gid.txt')
smx,smy,smyerr = importdata3col(r'E:\APS Data\Sector 15\Oct15 Data\2015oct\extracted_data\Qxy\Sm_701-706_qxy_gid.txt')


#Subtract flat background amount
yby = backgroundsubtract(yby)
ery = backgroundsubtract(ery)
dyy = backgroundsubtract(dyy)
tby = backgroundsubtract(tby)

ndy = backgroundsubtract(ndy)
pry = backgroundsubtract(pry)
cey = backgroundsubtract(cey)
smy = backgroundsubtract(smy)
lay = backgroundsubtract(lay)
euy = backgroundsubtract(euy)
gdy = backgroundsubtract(gdy)

#Normalize data
yby, ybyerr = normalizedata(yby, ybyerr)
ery, eryerr = normalizedata(ery, eryerr)
dyy, dyyerr = normalizedata(dyy, dyyerr)
tby, tbyerr = normalizedata(tby, tbyerr)

ndy, ndyerr = normalizedata(ndy, ndyerr)
pry, pryerr = normalizedata(pry, pryerr)
cey, ceyerr = normalizedata(cey, ceyerr)
smy, smyerr = normalizedata(smy, smyerr)
lay, layerr = normalizedata(lay, layerr)
euy, euyerr = normalizedata(euy, euyerr)
gdy, gdyerr = normalizedata(gdy, gdyerr)

##Set layout
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))

#Set x range
rangemin = max(ybx.min(),erx.min(),dyx.min(),tbx.min(),lax.min(),ndx.min(),eux.min(),gdx.min(),cex.min(),prx.min(),smx.min())
rangemax = min(ybx.max(),erx.max(),dyx.max(),tbx.max(),lax.max(),ndx.max(),eux.max(),gdx.max(),cex.max(),prx.max(),smx.max())

ax1.set_xlim([rangemin,rangemax])
ax2.set_xlim([rangemin,rangemax])

#Set y range
heightmaxh = max(yby.max(),ery.max(),dyy.max(),tby.max())
heightmaxl = max(cey.max(),ndy.max(),pry.max(),smy.max(),lay.max(),euy.max(),gdy.max())
ax1.set_ylim([0,1.1])
ax2.set_ylim([0,1.1])

#Hide tick labels for upper plot
plt.setp(ax1.get_xticklabels(),visible=False)

#Set axis labels
ax2.set_xlabel(r'$Q_{xy} (\AA^{-1})$')
ax1.text(0.2,0.2,'Intensity (arb.units)',rotation='vertical')

#Set minor tickmarks
ax1.set_xticks(np.arange(0.4,2.1,0.05),minor=True)
ax2.set_xticks(np.arange(0.4,2.1,0.05),minor=True)

#Set y tickmarks
ax1.set_yticks(np.arange(0,1.1,0.2))
ax2.set_yticks(np.arange(0,1.1,0.2))

#Add panel labels
ax1.text(0.46,0.95,'(a)')
ax2.text(0.46,0.95,'(b)')

#Add indices
ax1.text(0.56,0.6,r'$(10)I$',rotation='vertical')
ax1.text(1.38,0.7,r'$(10)M$',rotation='vertical')
ax1.annotate(r'$(11)M$',rotation='vertical',xy=(1.57,0.45),xytext=(1.67,0.7),arrowprops=dict(arrowstyle='->'))

ax2.text(1.56,0.7,r'$(11)M$',rotation='vertical')

##Do plots
ptsize=2
linew=0.5

ax1.plot(tbx,tby,marker='.',markersize=ptsize,linewidth=linew, label='Tb')
ax1.plot(dyx,dyy,marker='.',markersize=ptsize,linewidth=linew, label='Dy')
ax1.plot(erx,ery,marker='.',markersize=ptsize,linewidth=linew, label='Er')
ax1.plot(ybx,yby,marker='.',markersize=ptsize,linewidth=linew, label='Yb')
ax1.legend(loc=1,prop={'size':12})

ax2.plot(lax,lay,marker='.',markersize=ptsize,linewidth=linew, label='La')
ax2.plot(cex,cey,marker='.',markersize=ptsize,linewidth=linew, label='Ce')
ax2.plot(prx,pry,marker='.',markersize=ptsize,linewidth=linew, label='Pr')
ax2.plot(ndx,ndy,marker='.',markersize=ptsize,linewidth=linew, label='Nd')
ax2.plot(smx,smy,marker='.',markersize=ptsize,linewidth=linew, label='Sm')
ax2.plot(eux,euy,marker='.',markersize=ptsize,linewidth=linew, label='Eu')
ax2.plot(gdx,gdy,marker='.',markersize=ptsize,linewidth=linew, label='Gd')
ax2.legend(loc=1,prop={'size':12})

plt.savefig('DHDP_multiion.pdf',dpi=500)
plt.show()