import os
import numpy as np
import matplotlib.pyplot as plt

import InjectA



countyfilepath="/".join(InjectA.__file__.split('/')[0:-2])+"/data/Texas_County_XY.txt"

def addcounty_cmez(lon1=-104.7-0.1,lon2=-103.7+0.1,lat1=31.3-0.05,lat2=31.9+0.05):
	'''
	addcounty_cmez: add county lines in CMEZ area
	
	from pylib.plot import addcounty_cmez
	import matplotlib.pyplot as plt
	plt.figure()
	addcounty_cmez();
	plt.show()
	
	'''
	from matplotlib_scalebar.scalebar import ScaleBar # pip install matplotlib-scalebar
##red county lines
	f=open(countyfilepath,'r')
	# f=open('Culberson_XY.txt','r')
	clines=f.readlines()
	clines=[ii.rstrip().split(' ') for ii in clines]
	##add county lines
	tmp=[]
	for ii in range(len(clines)):
		if clines[ii] != ['']:
			tmp.append(clines[ii])
		else:
			tmp=np.array(tmp,dtype='float32')
			plt.plot(tmp[:,0],tmp[:,1],'-',color='#929591')
			ii=ii+1;
			tmp=[];
	plt.gca().set_xlim(lon1,lon2);plt.gca().set_ylim(lat1,lat2);
	plt.text(-104.4,31.3,'Culberson',fontsize=10,color='#929591')
	plt.text(-104.0,31.3,'Reeves',fontsize=10,color='#929591')
	scalebar = ScaleBar(110000,location='lower left');plt.gca().add_artist(scalebar)
	

def addcounty_tx():
	'''
	addcounty_tx: add state-scale county lines in Texas
	
	from pylib.plot import addcounty_tx
	import matplotlib.pyplot as plt
	plt.figure()
	addcounty_tx();
	plt.show()
	
	'''
	from pylib.io import asciiread
	##red county lines
	lines=asciiread(countyfilepath)
	lines=[ii.rstrip().split(' ') for ii in lines]
	##add county lines
	tmp=[]
	for ii in range(len(lines)):
		if lines[ii] != ['']:
			tmp.append(lines[ii])
		else:
			tmp=np.array(tmp,dtype='float32')
			plt.plot(tmp[:,0],tmp[:,1],'-',color='#929591')
			ii=ii+1;
			tmp=[];
	
	



	
	