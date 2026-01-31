import os
def get_well_loc(wellid,wellfile=None):
	"""
	get_well_loc: get lon,lat for a TexNet station
	
	Input
	wellid: str or list
	
	Output
	tuple (lon,lat) or a list of tuples (lonlats)
	
	Example 1:
	from InjectA import get_well_loc
	(lon,lat)=get_well_loc('120251')
	
	Example 2:
	from InjectA import get_well_loc
	lonlats=get_well_loc(['120251','66115'])
	
	Example 3:
	from InjectA import get_well_loc
	import matplotlib.pyplot as plt
	stas=['120251','66115']
	lonlats=get_well_loc(stas)
	for ii in lonlats:
		plt.plot(float(ii[0]),float(ii[1]),'d',color='r',markersize=15)
	for ii in range(len(stas)):
		plt.text(float(lonlats[ii][0]),float(lonlats[ii][1]),stas[ii],color='r')
	plt.plot(-102.0779,31.9973,'*b',markersize=12);
	plt.text(-102.0779,31.9973,'Midland',color='b',fontsize=14)
	plt.show()
	
	"""
	if wellfile is None:
		wellfile=os.getenv('HOME')+'/DATALIB/B3_injection_on20230329/Texas_Injection_Wells_V3/InjectionWell.csv'

	lines=open(wellfile).readlines();lines.pop(0);
	wellids=[str(ii.split(',')[0]) for ii in lines]
	welllats=[float(ii.split(',')[6]) for ii in lines]
	welllons=[float(ii.split(',')[7]) for ii in lines]
	
	print('number of wells in this file:', len(lines))

	if type(wellid) == str:
		i=wellids.index(wellid)
		return (welllons[i],welllats[i])
	elif type(wellid) == list:
		lonlats=[];
		for ista in range(len(wellid)):
			i=wellids.index(wellid[ista])
			lonlats.append((welllons[i],welllats[i]))
		return lonlats
	else:
		print('Wrong input parameter for get_well_loc');


def get_well_now(lat1=25,lat2=37,lon1=-107,lon2=-92,wellfile=None):
	"""
	get_well_now: get well ID that is in operation


	Example 1:
	from InjectA import get_well_now
	ids,lonlats=get_well_now()
	
	"""
	import pandas as pd
	
	if wellfile is None:
		wellfile=os.getenv('HOME')+'/DATALIB/B3_injection_on20230329/Texas_Injection_Wells_V3/InjectionWell.csv'
	
	data=pd.read_csv(wellfile)
	lats=data['SurfaceHoleLatitude']
	lons=data['SurfaceHoleLongitude']
	ic=0
	ids=[]
	for ii in range(len(data)):
		if lats[ii]<=lat2 and lats[ii]>=lat1 and lons[ii]<=lon2 and lons[ii]>=lon1:
			status=str(data['PermitStage'][ii]);
			print(status)
			if status != 'Not in Permitting Process':
				ids.append(str(data['InjectionWellId'][ii]))
				ic=ic+1
	print("%d wells are in AOI "%ic)
	
	return ids,get_well_loc(ids)
	
def get_well(lat1=25,lat2=37,lon1=-107,lon2=-92,wellfile=None):
	"""
	get_well: get well ID that is in a specific area defined by lat1/2 lon1/2


	Example 1:
	from InjectA import get_well
	ids,lonlats=get_well()
	
	"""
	import pandas as pd
	
	if wellfile is None:
		wellfile=os.getenv('HOME')+'/DATALIB/B3_injection_on20230329/Texas_Injection_Wells_V3/InjectionWell.csv'
	
	data=pd.read_csv(wellfile)
	lats=data['SurfaceHoleLatitude']
	lons=data['SurfaceHoleLongitude']
	ic=0
	ids=[]
	for ii in range(len(data)):
		if lats[ii]<=lat2 and lats[ii]>=lat1 and lons[ii]<=lon2 and lons[ii]>=lon1:
			status=str(data['PermitStage'][ii]);
			print(status)
# 			if status != 'Not in Permitting Process':
			ids.append(str(data['InjectionWellId'][ii]))
			ic=ic+1
	print("%d wells are in AOI "%ic)
	
	return ids,get_well_loc(ids)
	
	
def get_well_injectid(wellid,wellfile=None):
	"""
	get_well_injectid: get injectid


	Example 1:
	from InjectA import get_well_injectid
	data=get_well_injectid(111922)

	from InjectA import get_well_injectid
	data=get_well_injectid('111922')
	
	from InjectA import get_well_injectid
	data=get_well_injectid('128486')
	data[['Date']].to_numpy()
	data[['InjectedLiquidBBL']].to_numpy()
	
	data.loc[data['InjectedLiquidBBL']==0]
	
	import matplotlib.pyplot as plt
# 	plt.plot(data['Date'],data['InjectedLiquidBBL'])
# 	plt.show()
	"""
	import pandas as pd

	
	if wellfile is None:
		wellfile=os.getenv('HOME')+'/DATALIB/B3_injection_on20230329/Texas_Injection_Wells_V3/DailyInjection.csv'
	
	data=pd.read_csv(wellfile)
# 	dayid=data['DailyInjectionId']
# 	wellid=data['InjectionWellId']
# 	time=data['Date']
# 	InjectedLiquidBBL=data['InjectedLiquidBBL']
# 	LiquidInjectionVolumeUtilization=data['LiquidInjectionVolumeUtilization']
# 	InjectedPSIG=data['InjectedPSIG']
# 	MaxDailyInjectionPSIG=data['MaxDailyInjectionPSIG']
	
	dataout=data.loc[data['InjectionWellId']==int(wellid)][['DailyInjectionId','InjectionWellId','Date','InjectedLiquidBBL']]

	
	return dataout
	
	