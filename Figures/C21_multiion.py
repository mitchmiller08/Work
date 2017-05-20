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
	
def normalizec21data(y,error,stacks):

	max = 0
	for row in y:
		if row.max() > max:
			max = row.max()
	
	i=0
	for row in y:
		y[i] = y[i] / (max*stacks)
		i += 1
	
	i=0
	for row in error:
		error[i] = error[i] / (max*stacks)
		i += 1
	
	return y, error
	
##Import data
#Heavy
erscans = range(21,28+1,1)
erx,ery,eryerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Er_C21_21-28\Er_C21_S# ','_F# 0_cut.txt',erscans)
euscans = range(131,139+1,1)
eux,euy,euyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Eu_C21_131-139\Eu_C21_S# ','_F# 0_cut.txt',euscans)
gdscans = range(121,129+1,1)
gdx,gdy,gdyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Gd_C21_121-129\Gd_C21_S# ','_F# 0_cut.txt',gdscans)
tbscans = range(91,99+1,1)
tbx,tby,tbyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Tb_C21_91-99\Tb_C21_S# ','_F# 0_cut.txt',tbscans)
dyscans = range(81,89+1,1)
dyx,dyy,dyyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Dy_C21_81-89\Dy_C21_S# ','_F# 0_cut.txt',dyscans)
ybscans = range(71,79+1,1)
ybx,yby,ybyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Yb_C21_71-79_HP25\Yb_C21_S# ','_F# 0_cut.txt',ybscans)

#Delete overlapping scans (5th scan)
del eux[4],euy[4],euyerr[4]
del gdx[4],gdy[4],gdyerr[4]
del tbx[4],tby[4],tbyerr[4]
del dyx[4],dyy[4],dyyerr[4]
del ybx[4],yby[4],ybyerr[4]

heavy = [[eux,euy,euyerr],[gdx,gdy,gdyerr],[tbx,tby,tbyerr],[dyx,dyy,dyyerr],[erx,ery,eryerr],[ybx,yby,ybyerr]]

#Light
prscans = range(304,312+1,1)
prx,pry,pryerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Pr_C21_304-312\Pr_C21_S# ','_F# 0_cut.txt',prscans)
ndscans = range(141,149+1,1)
ndx,ndy,ndyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Nd_141-149\QxyProfiles\Backup\Nd_C21_S# ','_F# 0_cut.txt',ndscans)
cescans = range(324,332+1,1)
cex,cey,ceyerr = importc21('E:\APS Data\Sector 15\Jun15 Data\extracted_data\Ce_C21_324-332\Ce_C21_S# ','_F# 0_cut.txt',cescans)

#Delete overlapping scans (5th scan)
del cex[4],cey[4],ceyerr[4]
del prx[4],pry[4],pryerr[4]
del ndx[4],ndy[4],ndyerr[4]


light = [[cex,cey,ceyerr],[prx,pry,pryerr],[ndx,ndy,ndyerr]]

##Strip data
#Heavy
for element in heavy:
	element[0][0],element[1][0],element[2][0] = stripdata(0.515,0.60,element[0][0],element[1][0],element[2][0])
	element[0][1],element[1][1],element[2][1] = stripdata(0.82,0.9,element[0][1],element[1][1],element[2][1])
	element[0][2],element[1][2],element[2][2] = stripdata(1.025,1.12,element[0][2],element[1][2],element[2][2])
	element[0][3],element[1][3],element[2][3] = stripdata(1.24,1.355,element[0][3],element[1][3],element[2][3])
	element[0][4],element[1][4],element[2][4] = stripdata(1.35,1.54,element[0][4],element[1][4],element[2][4])
	element[0][5],element[1][5],element[2][5] = stripdata(1.55,1.8,element[0][5],element[1][5],element[2][5])
	element[0][6],element[1][6],element[2][6] = stripdata(1.81,1.86,element[0][6],element[1][6],element[2][6])
#	element[0][7],element[1][7],element[2][7] = stripdata(2.15,1.86,element[0][7],element[1][7],element[2][7])
#	element[0][6],element[1][6],element[2][6] = stripdata(1.81,2.03,element[0][6],element[1][6],element[2][6])		Old ranges
#	element[0][7],element[1][7],element[2][7] = stripdata(2.15,2.34,element[0][7],element[1][7],element[2][7])		Old ranges
	del element[0][7],element[1][7],element[2][7]
	element[1], element[2] = normalizec21data(element[1], element[2],6)
	
#Light
for element in light:
	element[0][0],element[1][0],element[2][0] = stripdata(0.494,0.60,element[0][0],element[1][0],element[2][0])
	element[0][1],element[1][1],element[2][1] = stripdata(0.8,0.98,element[0][1],element[1][1],element[2][1])
	element[0][2],element[1][2],element[2][2] = stripdata(1.0,1.21,element[0][2],element[1][2],element[2][2])
	element[0][3],element[1][3],element[2][3] = stripdata(1.22,1.4,element[0][3],element[1][3],element[2][3])
	element[0][4],element[1][4],element[2][4] = stripdata(1.39,1.59,element[0][4],element[1][4],element[2][4])
	element[0][5],element[1][5],element[2][5] = stripdata(1.58,1.79,element[0][5],element[1][5],element[2][5])
	element[0][6],element[1][6],element[2][6] = stripdata(1.77,1.86,element[0][6],element[1][6],element[2][6])
#	element[0][7],element[1][7],element[2][7] = stripdata(2.1,1.86,element[0][7],element[1][7],element[2][7])
#	element[0][6],element[1][6],element[2][6] = stripdata(1.77,2.03,element[0][6],element[1][6],element[2][6])		Old ranges
#	element[0][7],element[1][7],element[2][7] = stripdata(2.1,2.5,element[0][7],element[1][7],element[2][7])		Old ranges
	del element[0][7],element[1][7],element[2][7]
	element[1], element[2] = normalizec21data(element[1], element[2],3)
	
##Set plot layout
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))

#Set x range (set by data stripping)
ax1.set_xlim([0.45,1.9])
ax2.set_xlim([0.45,1.9])

#Set y range (including offset)
heavyoffset = 8000
ax1.set_ylim([0,1.1])
lightoffset = 8000
ax2.set_ylim([0,1.1])

#Hide tick labels for upper plot
plt.setp(ax1.get_xticklabels(),visible=False)

#Set x tickmarks
ax1.set_xticks(np.arange(0.4,2.1,0.05),minor=True)
ax2.set_xticks(np.arange(0.4,2.1,0.05),minor=True)

#Set axis labels
ax2.set_xlabel(r'$Q_{xy} (\AA^{-1})$')
ax1.text(0.18,0.15,'Intensity (arb.units)',rotation='vertical')

#Add element labels
ax1.text(1.9,0.2/6,'Eu')
ax1.text(1.9,1.2/6,'Gd')
ax1.text(1.9,2.2/6,'Tb')
ax1.text(1.9,3.2/6,'Dy')
ax1.text(1.9,4.2/6,'Er')
ax1.text(1.9,5.2/6,'Yb')

ax2.text(1.9,0.2/3,'Ce')
ax2.text(1.9,1.2/3,'Pr')
ax2.text(1.9,2.2/3,'Nd')

#Add panel labels
ax1.text(0.43,0.95,'(a)')
ax2.text(0.43,0.95,'(b)')


#Add peak lines (heavy)
ax1.axvline(x=0.544,color='black',linewidth=0.2)
ax1.axvline(x=0.854,color='black',linewidth=0.2)
ax1.axvline(x=1.082,color='black',linewidth=0.2)
ax1.axvline(x=1.252,color='black',linewidth=0.2)
ax1.axvline(x=1.342,color='black',linewidth=0.2)
ax1.axvline(x=1.599,color='black',linewidth=0.2)
ax1.axvline(x=1.680,color='black',linewidth=0.2)

#Add peak lines (light)
ax2.axvline(x=0.511,color='black',linewidth=0.2)
ax2.axvline(x=0.906,color='black',linewidth=0.2)
ax2.axvline(x=1.018,color='black',linewidth=0.2)
ax2.axvline(x=1.038,color='black',linewidth=0.2)
ax2.axvline(x=1.359,color='black',linewidth=0.2)
ax2.axvline(x=1.381,color='black',linewidth=0.2)
ax2.axvline(x=1.444,color='black',linewidth=0.2)
ax2.axvline(x=1.518,color='black',linewidth=0.2)
ax2.axvline(x=1.554,color='black',linewidth=0.2)
ax2.axvline(x=1.681,color='black',linewidth=0.2)
ax2.axvline(x=1.760,color='black',linewidth=0.2)
ax2.axvline(x=1.804,color='black',linewidth=0.2)

#Add indices
plt.figtext(0.18,0.95,'$(10)I$',rotation='vertical')
plt.figtext(0.325,0.95,r'$(\frac{1}{2}\frac{1}{2})C$',rotation='vertical')
plt.figtext(0.435,0.95,'$(02)I$',rotation='vertical')
plt.figtext(0.505,0.945,r'$(\frac{1}{2}\overline{\frac{1}{2}})C$',rotation='vertical')
plt.figtext(0.555,0.965,'$(10)M$',rotation='vertical')
plt.figtext(0.675,0.965,'$(01)M$',rotation='vertical')
plt.figtext(0.715,0.965,'$(11)M$',rotation='vertical')

plt.figtext(0.165,0.51,'$(10)I$',rotation='vertical')
plt.figtext(0.35,0.51,'$(21)I$',rotation='vertical')
plt.figtext(0.395,0.51,'$(02)I$',rotation='vertical')
plt.figtext(0.42,0.51,'$(02)I$',rotation='vertical')
plt.figtext(0.555,0.51,'$(13)I$',rotation='vertical')
plt.figtext(0.58,0.51,'$(31)I$',rotation='vertical')
plt.figtext(0.605,0.515,r'$(01)M$',rotation='vertical', size=10)
plt.figtext(0.655,0.51,'$(30)I$',rotation='vertical')
plt.figtext(0.72,0.51,'$(11)M$',rotation='vertical', size=10)
plt.figtext(0.75,0.505,r'$(2\overline{2})I$',rotation='vertical')
plt.figtext(0.775,0.51,'$(42)I$',rotation='vertical')
ax2.annotate('$(01)M$\n$(03)I$',rotation='vertical',xy=(1.52,1.05),xytext=(1.88,1.1),arrowprops=dict(arrowstyle='->',connectionstyle="angle,angleA=90,angleB=0,rad=10"),bbox=dict(boxstyle='round',fc='white'))


##Do plots
#Set parameters
colorlist = ['blue','red','green','black','orange','purple']
ptsize=2
linew=0.5

#Plot all heavy elements
j=0
for element in heavy:
	i = 0
	while i < len(element[0]):
		ax1.plot(element[0][i],element[1][i]+j/6.,marker='.',markersize=ptsize,linewidth=linew,color=colorlist[j])
		i = i + 1
	j = j + 1

#Plot all light elements	
j=0
for element in light:
	i = 0
	while i < len(element[0]):
		ax2.plot(element[0][i],element[1][i]+j/3.,marker='.',markersize=ptsize,linewidth=linew,color=colorlist[j])
		i = i + 1
	j = j + 1

plt.savefig('C21_multiion.pdf',dpi=500)
plt.show()