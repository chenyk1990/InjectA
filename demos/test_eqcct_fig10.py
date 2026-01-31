import os
import numpy as np


from InjectA import asciiread
from InjectA import addcounty_cmez
from InjectA import get_well_now
from InjectA import get_well
from InjectA import get_well_injectid
from InjectA import get_well_loc
from InjectA import win_catalog
from InjectA import eventlist

from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import obspy.core.utcdatetime as utc

list202210=[ '2022-10-%02d'%(ii+1) for ii in range(31)]


lon1=-104.7
lon2=-103.9
lat1=31.5
lat2=31.8
radius=0.1
# radius=0.25
# radius=0.5

ids,lonlats=get_well_now(lat1=lat1,lat2=lat2,lon1=lon1,lon2=lon2);


ids2,lonlats2=get_well(lat1=lat1,lat2=lat2,lon1=lon1,lon2=lon2);


plt.plot([ii[0] for ii in lonlats2],[ii[1] for ii in lonlats2],'d',color='g',markersize=6)
plt.plot([ii[0] for ii in lonlats],[ii[1] for ii in lonlats],'d',color='r',alpha=0.5,markersize=6)

for ii in range(len(ids2)):
	plt.text(lonlats2[ii][0],lonlats2[ii][1],ids2[ii],fontsize=8)
	
addcounty_cmez()
plt.savefig('wells202210.png',format='png',dpi=300)
plt.show()

## Plot
t1=float(utc.UTCDateTime(2022,10,1,0,0,0,0));
t2=float(utc.UTCDateTime(2022,11,1,0,0,0,0))
x0=float(utc.UTCDateTime(2022,10,27,0,0,0,0));
x00=float(utc.UTCDateTime(2022,10,22,0,0,0,0));


vol=[]
for ii in range(31):
	vol.append(0)

ik=-1
ids3=[]
volall=[]
vol1=[] #well 1
for kk in ids2:
	ik=ik+1;
	vol=[]
	times=[]
	data=get_well_injectid(kk)
	for ii in range(len(list202210)):
# 		print(list202210[ii])
	
		if list202210[ii] in data[['Date']].to_numpy():
			jj=np.argwhere(data[['Date']].to_numpy()==list202210[ii])[0,0]
			vol.append(float(data[['InjectedLiquidBBL']].to_numpy()[jj]))
			if kk == '128486':
				vol1.append(float(data[['InjectedLiquidBBL']].to_numpy()[jj]))
		else:
			vol.append(float(0))
			if kk == '128486':
				vol1.append(float(0))
		times.append(utc.UTCDateTime(2022, 10, ii+1, 00, 00, 00, 000000))
		
		
	times=[float(ii) for ii in times]
	
	if np.array(vol).max()>0:
		print(kk)
		
		ids3.append(kk)
		
# 		times=np.array(times)
# 		vol=np.array(vol)
		volall.append(vol);
		
# 		plt.plot(times,vol,label=kk,color='k')
# 		plt.legend(loc='lower right')
# 		plt.gca().set_ylabel("Volume (bbl)",fontsize='medium', fontweight='normal')
# 		plt.xticks([])
# 		y1,y2=plt.gca().get_ylim()
# 		plt.plot([x0,x0],[y1,y2],color='r',linestyle='dashed',linewidth=2)
# 		plt.gca().set_xlim(xmin=t1,xmax=t2)
# 		plt.gca().legend(loc='center left');
# 		plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.e'))
# 		plt.plot([x00,x00],[y1,y2],color='b',linestyle='dashed',linewidth=2)
# 		
# 		plt.savefig('wells202210_injection_%s.png'%kk,format='png',dpi=300)
# 		plt.show()
# 		times.append(utc.UTCDateTime(2022, 10, ii+1, 00, 00, 00, 000000))
		
# 		print(vol)
lonlats3=get_well_loc(ids3)

ic=0;
volnew=0;
for ii in range(len(lonlats3)):
	if np.power(np.power(lonlats3[ii][0]-lonlats[0][0],2)+np.power(lonlats3[ii][1]-lonlats[0][1],2),0.5)<=radius:
		ic=ic+1
		volnew=volnew+np.array(volall[ii])
print('Well NO is',ic)

plt.figure()
plt.plot(times,volnew,label=kk,color='k')
plt.show()


plt.figure()
plt.plot([ii[0] for ii in lonlats3],[ii[1] for ii in lonlats3],'d',color='g',markersize=6)
plt.plot([ii[0] for ii in lonlats[0:1]],[ii[1] for ii in lonlats[0:1]],'d',color='r',alpha=0.5,markersize=6)

for ii in range(len(ids3)):
	plt.text(lonlats3[ii][0],lonlats3[ii][1],ids3[ii],fontsize=8)
	
addcounty_cmez()

# radius=0.25
# radius=0.05

for ii in range(len(ids[0:1])):
# 	plt.text(lonlats[ii][0],lonlats[ii][1]+0.04*(ii-0.5),{'128486':'Well 1','128485':'Well 2'}[ids[ii]])
	circle1=plt.Circle((lonlats[ii][0],lonlats[ii][1]),radius,color='lightyellow')
	plt.gca().add_patch(circle1)
# 	plt.plot([lonlats[ii][0],lonlats[ii][0]],[lonlats[ii][1],lonlats[ii][1]+0.04*(ii-0.5)],color='r')

plt.savefig('wells202210_locs_%sdeg.png'%str(radius),format='png',dpi=300)
plt.show()

# 	times=[float(ii) for ii in times]

## NEW 
## second EQCCT catalog
fname='../data/delaware202210xml11777.csv'
lines=asciiread(fname)
lines.pop(0)
lons1=[float(ii.split(',')[9]) for ii in lines]
lats1=[float(ii.split(',')[8]) for ii in lines]
deps1=[float(ii.split(',')[10]) for ii in lines]
ids1=[ii.split(',')[0].split('/')[-1] for ii in lines]
mags1=[float(ii.split(',')[7]) for ii in lines]
rmss1=[float(ii.split(',')[-1]) for ii in lines]
utcs1=[utc.UTCDateTime(ii.split(',')[6].split(' ')[0]+'T'+ii.split(',')[6].split('+')[0].split(' ')[1]) for ii in lines]
#[ii for ii in lines if float(ii.split(',')[4])>3.5] #mag > 3.5
utcs1=[float(ii) for ii in utcs1]

utcs11=[float(utcs1[ii]) for ii in range(len(utcs1)) if np.power(np.power(lons1[ii]-lonlats[0][0],2)+np.power(lats1[ii]-lonlats[0][1],2),0.5)<=radius]
# utcs22=[float(utcs2[ii]) for ii in range(len(utcs2)) if np.power(np.power(lons2[ii]-lonlats[0][0],2)+np.power(lats2[ii]-lonlats[0][1],2),0.5)<=radius]




lon1=-104.7
lon2=-103.9
lat1=31.5
lat2=31.8

eids=win_catalog(fincatalog=None,foutcatalog=None,time_beg=None,time_end=None,lon_beg=lon1,lon_end=lon2,lat_beg=lat1,lat_end=lat2,t1=202210,t2=202211)
lines=eventlist(eids,fincatalog=None)
lines.pop(0)
#[ii for ii in lines if float(ii.split(',')[4])>3.5] #mag > 3.5

lats3=[float(ii.split(',')[6]) for ii in lines]
lons3=[float(ii.split(',')[8]) for ii in lines]
deps3=[float(ii.split(',')[10]) for ii in lines]
mags3=[float(ii.split(',')[4]) for ii in lines]
rmss3=[float(ii.split(',')[13]) for ii in lines]
utcs3=[utc.UTCDateTime(ii.split(',')[2]+'T'+ii.split(',')[3]) for ii in lines]

utcs3=[float(ii) for ii in utcs3]
# plt.hist(utcs2,31,range=(np.min(utcs2),np.max(utcs2)),label='EQCCT (three months)',color='lightgray',edgecolor='black',log=True)
# plt.plot(utcs2,mags2,)
utcs3=[ float(utcs3[ii]) for ii in range(len(deps3)) if np.power(np.power(lons3[ii]-lonlats[0][0],2)+np.power(lats3[ii]-lonlats[0][1],2),0.5)<=radius]
mags3=[ float(mags3[ii]) for ii in range(len(deps3)) if np.power(np.power(lons3[ii]-lonlats[0][0],2)+np.power(lats3[ii]-lonlats[0][1],2),0.5)<=radius]



plt.figure(figsize=(12, 8))
plt.subplot(2,2,1)

lon1=-104.7
lon2=-103.9
lat1=31.5
lat2=31.8
# radius=0.1
# radius=0.05
# radius=0.1

plt.plot(lons1,lats1,'.',color='k',markersize=1,label='Event')
plt.gca().set_ylim(ymin=lat1,ymax=lat2);
plt.gca().set_xlim(xmin=lon1,xmax=lon2);
plt.setp(plt.gca().get_xticklabels(), visible=True)
plt.gca().set_ylabel("Latiitude (deg)",fontsize='large', fontweight='normal')
plt.gca().set_xlabel("Longitude (deg)",fontsize='large', fontweight='normal')
# plt.title('EQCCT')
addcounty_cmez();

plt.plot([ii[0] for ii in lonlats3],[ii[1] for ii in lonlats3],'d',color='g',markersize=6,label='Injecting wells')
plt.plot([ii[0] for ii in lonlats[0:1]],[ii[1] for ii in lonlats[0:1]],'d',color='r',alpha=0.5,markersize=6,label='Well 1')
for ii in range(len(ids[0:1])):
# 	plt.text(lonlats[ii][0],lonlats[ii][1]+0.04*(ii-0.5),{'128486':'Well 1','128485':'Well 2'}[ids[ii]])
	circle1=plt.Circle((lonlats[ii][0],lonlats[ii][1]),radius,color='yellow')
	plt.gca().add_patch(circle1)

plt.gca().legend(loc='upper left');
plt.gca().text(lon1-0.3, lat2+0.15, "(a)", fontsize=16, color='k')

# plt.subplot(2,2,3)
# plt.plot(lons2,lats2,'.',color='k',markersize=1)
# plt.gca().set_ylim(ymin=lat1,ymax=lat2);
# plt.gca().set_xlim(xmin=lon1,xmax=lon2);
# plt.setp(plt.gca().get_xticklabels(), visible=True)
# plt.gca().set_ylabel("Latiitude (deg)",fontsize='large', fontweight='normal')
# plt.gca().set_xlabel("Longitude (deg)",fontsize='large', fontweight='normal')
# plt.title('TexNet')
# addcounty_cmez();
# plt.plot([ii[0] for ii in lonlats3],[ii[1] for ii in lonlats3],'d',color='g',markersize=6)
# plt.plot([ii[0] for ii in lonlats],[ii[1] for ii in lonlats],'d',color='r',alpha=0.5,markersize=6)
# for ii in range(len(ids[0:2])):
# # 	plt.text(lonlats[ii][0],lonlats[ii][1]+0.04*(ii-0.5),{'128486':'Well 1','128485':'Well 2'}[ids[ii]])
# 	circle1=plt.Circle((lonlats[ii][0],lonlats[ii][1]),radius,color='r')
# 	plt.gca().add_patch(circle1)

plt.subplot(3,2,2)
t1=float(utc.UTCDateTime(2022,10,1,0,0,0,0));
t2=float(utc.UTCDateTime(2022,11,1,0,0,0,0))
p1=plt.hist(utcs11,31,range=(t1,t2),label='EQCCT (one month)',color='lightgray',edgecolor='black',log=True)
# plt.hist(utcs22,31,range=(t1,t2),label='EQCCT 2 (one month)',color='lightyellow',edgecolor='black',alpha=0.5,log=True)

plt.gca().set_xlim(xmin=t1,xmax=t2)

plt.gca().set_ylabel("Number",fontsize='small', fontweight='normal')
plt.xticks([])
# plt.gca().set_ylim(ymin=0,ymax=100)
# x1,x2=plt.gca().get_xlim()
# plt.xticks([x1, (x1+x2)/2, x2], ['Oct 1 2022', 'Oct 16 2022', 'Nov 1 2022'])
# plt.gca().set_xlabel("Time",fontsize='medium', fontweight='normal')
# plt.gca().legend(handles=p2+p3,loc='lower left');

x0=float(utc.UTCDateTime(2022,10,27,0,0,0,0));
x00=float(utc.UTCDateTime(2022,10,22,0,0,0,0));
y1,y2=plt.gca().get_ylim();
y2=y2*1.1;y1=0;

plt.gca().set_ylim(ymin=y1,ymax=y2)
plt.plot([x0,x0],[y1,y2],color='r',linestyle='dashed',linewidth=2)
plt.plot([x00,x00],[y1,y2],color='b',linestyle='dashed',linewidth=2)
plt.text(x0,y2-15,'10/27 0:0:0',color='r',fontsize='small')
plt.text(x00,y2-15,'10/22 0:0:0',color='b',fontsize='small')

rec=[Rectangle([x0,y1],width=(x0-x00)/5,height=(y2-y1))]
pc=PatchCollection(rec, facecolor='r', alpha=0.2,edgecolor='r')
plt.gca().add_collection(pc)
# plt.show()
plt.gca().text(t1-0.00025*t1, y2+y2*0.1, "(b)", fontsize=16, color='k')


plt.subplot(3,2,4)

plt.scatter(utcs3,mags3,s=mags3,facecolor='red',edgecolor='k',alpha=0.9,label='TexNet')#c=
plt.gca().set_ylabel("Magnitude",fontsize='medium', fontweight='normal')
# plt.gca().set_xlabel("Time",fontsize='large', fontweight='normal')
plt.gca().set_xlim(xmin=t1,xmax=t2)

# x1,x2=plt.gca().get_xlim()
# plt.xticks([x1, (x1+x2)/2, x2], ['Oct 1 2022', 'Oct 16 2022', 'Oct 31 2022'])
# plt.show()
plt.setp(plt.gca().get_xticklabels(), visible=False)
y1,y2=plt.gca().get_ylim()
y1=0;y2=4.0;
plt.plot([x0,x0],[y1,y2],color='r',linestyle='dashed',linewidth=2)
plt.plot([x00,x00],[y1,y2],color='b',linestyle='dashed',linewidth=2)
plt.xticks([])


## plot EQCCT smaller events
Mthr=1.8 #(threshold)
x1,x2=plt.gca().get_xlim()
plt.plot([x1,x2],[Mthr,Mthr],color='m',linestyle='dashed',linewidth=2)
plt.text(x1,Mthr+0.2,'Texnet magnitude threshold',color='m',fontsize='small')

utcs1=[ utcs1[ii] for ii in range(len(mags1)) if mags1[ii]<=Mthr and np.power(np.power(lons1[ii]-lonlats[0][0],2)+np.power(lats1[ii]-lonlats[0][1],2),0.5)<=radius]
mags1=[ mags1[ii] for ii in range(len(mags1)) if mags1[ii]<=Mthr and np.power(np.power(lons1[ii]-lonlats[0][0],2)+np.power(lats1[ii]-lonlats[0][1],2),0.5)<=radius]

plt.scatter(utcs1,mags1,s=1,facecolor='red',edgecolor='g',alpha=0.9,label='EQCCT')
plt.gca().set_xlim(xmin=t1,xmax=t2)
plt.gca().set_ylim(ymin=y1,ymax=y2)
plt.gca().legend(loc='lower left');


rec=[Rectangle([x0,y1],width=(x0-x00)/5,height=(y2-y1))]
pc=PatchCollection(rec, facecolor='r', alpha=0.2,edgecolor='r')
plt.gca().add_collection(pc)

plt.gca().text(t1-0.00025*t1, y2+y2*0.1, "(c)", fontsize=16, color='k')

ax=plt.subplot(3,2,6)
p1,=plt.plot(np.array(times)+43200.0,volnew,'k-s',label='Total injection',color='k')
# plt.plot(times,vol1,label='Well 1',color='r')
# plt.legend(loc='lower right')
ax.set_ylabel("Volume (bbl)",fontsize='medium', fontweight='normal')
plt.xticks([])
y1,y2=plt.gca().get_ylim()
ax.plot([x0,x0],[y1,y2],color='r',linestyle='dashed',linewidth=2)
plt.gca().set_xlim(xmin=t1,xmax=t2)
# plt.gca().legend(loc='center left');
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.e'))
plt.plot([x00,x00],[y1,y2],color='b',linestyle='dashed',linewidth=2)

ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Volume (bbl)', color='g')  # we already handled the x-label with ax1
p2,=ax2.plot(np.array(times)+43200.0,vol1,'g-s', color='g', label='Well 1 injection')
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.e'))
ax2.yaxis.label.set_color('g')

lines=[p1,p2]
plt.gca().legend(lines, [l.get_label() for l in lines])


y11,y22=plt.gca().get_ylim()
y1=min(y1,y11);#y2=max(y2,y22);
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
rec=[Rectangle([x0,y1],width=(x0-x00)/5,height=(y2-y1)*1.1)]
pc=PatchCollection(rec, facecolor='r', alpha=0.2,edgecolor='r')
ax.add_collection(pc)
# plt.legend(loc='lower left');

# plt.show()
# plt.plot(times,vol,label={'128486':'Well 1','128485':'Well 2'}[kk],color='k')
# plt.subplot(4,2,8)
# # plt.plot(times,volnew,label='Total injection',color='k')
# plt.plot(times,vol1,label='Well 1',color='r')
# plt.legend(loc='lower right')
# plt.gca().set_ylabel("Volume (bbl)",fontsize='medium', fontweight='normal')
# plt.xticks([])
# y1,y2=plt.gca().get_ylim()
# plt.plot([x0,x0],[y1,y2],color='r',linestyle='dashed',linewidth=2)
# plt.gca().set_xlim(xmin=t1,xmax=t2)
# plt.gca().legend(loc='center left');
# plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.e'))
# plt.plot([x00,x00],[y1,y2],color='b',linestyle='dashed',linewidth=2)

x1,x2=plt.gca().get_xlim()
plt.xticks([x1, (x1+x2)/2, x2], ['Oct 1 2022', 'Oct 16 2022', 'Nov 1 2022'])
plt.gca().set_xlabel("Time",fontsize='medium', fontweight='normal')

ax.text(t1-0.00025*t1, y2+y2*0.01, "(d)", fontsize=16, color='k')


plt.savefig('test_eqcct_fig10_temporal_%sdeg.png'%str(radius),format='png',dpi=300)

plt.show()
