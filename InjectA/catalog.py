import os

def create_catalog(eids,fincatalog=None,foutcatalog=None):
	"""
	Create TexNet style catalog from event list eids
	Written by Yangkang Chen
	Oct, 19, 2022
	
	INPUT
	eids:
	fcatalog: Input (complete) Texas Catalog
	
	OUTPUT
	foutcatalog: a csv catalog file written on the disk
	
	Example
	from InjectA import create_catalog
	eids=['texnet2020galz']
	create_catalog(eids)
	"""
	from pylib.io import asciiwrite
	
	if fincatalog is None:
		fincatalog=os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_events_20240201.csv';
	
	if foutcatalog is None:
		foutcatalog='./newcatalog.csv'
	
	f=open(fincatalog);
	lines=f.readlines();
	
	lines2=[]
	lines2.append(lines[0])
	for ii in range(len(lines)-1):
		if lines[ii+1].split(',')[0] in eids:
			lines2.append(lines[ii+1])
	asciiwrite(foutcatalog,lines2,withnewline=True)
	
	
def catalog2eids(fincatalog=None,feids=None):
	"""
	Transform TexNet style catalog to event list (eids) in ASCII format
	Written by Yangkang Chen
	Oct, 20, 2022
	
	INPUT
	eids:
	fcatalog: Input (complete) Texas Catalog
	
	OUTPUT
	foutcatalog: a csv catalog file written on the disk
	
	Example
	from InjectA import catalog2eids
	eids=catalog2eids(fincatalog=None);
	"""
	from pylib.io import asciiwrite
	
	if fincatalog is None:
		fincatalog=os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_events_20240201.csv';
	
	if feids is None:
		feids='./eids.txt'
	
	f=open(fincatalog);
	lines=f.readlines();
	lines.pop(0)
	
	eids=[ii.split(',')[0] for ii in lines]
	asciiwrite(feids,eids,withnewline=False)

	return eids
	
	
def read_events(eids):
	"""
	Read events according to input eids list
	
	INPUT
	Eventid list (eids)
	
	OUTPUT
	catalog obj (cat)
	
	Example
	from InjectA import read_events as my_events
	
	eids=['texnet2020galz','texnet2020gcua']
	cat=my_events(eids)
	cat.plot()
	
	"""
	import obspy
	from obspy.clients.fdsn import Client
	
	cat=obspy.Catalog()
	for ie in eids:
		print('Event id: ', ie)
		try:
			c=obspy.read_events(os.getenv('HOME')+'/DATALIB/TexNet-refined-database-catalog-PSpicks-EVENTS/'+ie+'.qml')
		except:
			try:
				cl = Client('http://rtserve.beg.utexas.edu')
				c = cl.get_events(eventid=ie, includearrivals=True)
			except:
				try:
					cl = Client('http://rtserve.beg.utexas.edu')
					c = cl.get_events(eventid=ie)
				except:
					try:
						cl = Client('http://sc3primary.beg.utexas.edu')
						c = cl.get_events(eventid=ie, includearrivals=True)
					except:
						try:
							cl = Client('http://scdb.beg.utexas.edu')
							c = cl.get_events(eventid=ie, includearrivals=True)
						except:
							print('Not downloadable')
		cat.append(c[0])
	return cat

def eventlist(eids,fincatalog=None):
	"""
	Read events according to input eids list
	
	INPUT
	Eventid list (eids)
	
	OUTPUT
	list (cat)
	
	Example
	from InjectA import eventlist as myevelist
	eids=['texnet2020galz','texnet2020gcua']
	e=myevelist(eids)
	
	"""
	import obspy
	from obspy.clients.fdsn import Client

	if fincatalog is None:
		fincatalog=os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_events_20240201.csv';
	
	f=open(fincatalog);
	lines=f.readlines();
	
	# add the first line
	cat=[]
	cat.append(lines[0].strip())

	# remove the first line
	lines.pop(0) #or lines=lines[1:]
	eids0=[ii.split(',')[0] for ii in lines]
	
	# find the event
	for ii in eids:
		cat.append(lines[eids0.index(ii)].strip())
	
	return cat

def get_ev_loc(eid,fincatalog=None):
	"""
	Get event location
	
	INPUT
	Eventid list (eids)
	
	OUTPUT
	list (cat)
	
	Example
	from InjectA import get_ev_loc
	eid='texnet2020galz'
	lon,lat,dep=get_ev_loc(eid)
	
	"""
	import obspy
	from obspy.clients.fdsn import Client

	if fincatalog is None:
		fincatalog=os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_events_20240201.csv';
	
	f=open(fincatalog);
	lines=f.readlines();
	
	# add the first line
	cat=[]
	cat.append(lines[0].strip())

	# remove the first line
	lines.pop(0) #or lines=lines[1:]
	eids0=[ii.split(',')[0] for ii in lines]
	
	# find the event
	cat.append(lines[eids0.index(eid)].strip())
	
	lon=float(lines[eids0.index(eid)].split(',')[8])
	lat=float(lines[eids0.index(eid)].split(',')[6])
	dep=float(lines[eids0.index(eid)].split(',')[10])
	mag=float(lines[eids0.index(eid)].split(',')[4])
	
	return lon,lat,dep

def get_ev_locmag(eid,fincatalog=None):
	"""
	Get event location
	
	INPUT
	Eventid list (eids)
	
	OUTPUT
	list (cat)
	
	Example
	from InjectA import get_ev_locmag
	eid='texnet2020galz'
	lon,lat,dep,mag=get_ev_locmag(eid)
	
	"""
	import obspy
	from obspy.clients.fdsn import Client

	if fincatalog is None:
		fincatalog=os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_events_20240201.csv';
	
	f=open(fincatalog);
	lines=f.readlines();
	
	# add the first line
	cat=[]
	cat.append(lines[0].strip())

	# remove the first line
	lines.pop(0) #or lines=lines[1:]
	eids0=[ii.split(',')[0] for ii in lines]
	
	# find the event
	cat.append(lines[eids0.index(eid)].strip())
	
	lon=float(lines[eids0.index(eid)].split(',')[8])
	lat=float(lines[eids0.index(eid)].split(',')[6])
	dep=float(lines[eids0.index(eid)].split(',')[10])
	mag=float(lines[eids0.index(eid)].split(',')[4])
	
	return lon,lat,dep,mag
	
def win_catalog(fincatalog=None,foutcatalog=None,time_beg=None,time_end=None,lon_beg=None,lon_end=None,lat_beg=None,lat_end=None,t1=None,t2=None):
	'''
	Window a catalog according to the given beg/end time, beg/end lon and beg/end lat (AOI)
	
	INPUT
	fincatalog: input catalog
	time_beg/time_end: 	beg/end time
	lon_beg/lon_end: 	beg/end lon
	lat_beg/lat_end: 	beg/end lat
	t1: simple time_beg input of year/month/day in the format of 20221001
	t2: simple time_end input of year/month/day in the format of 20221101
	
	OUTPUT
	foutcatalog: output catalog
	
	Example
	
	Example1
	from InjectA import win_catalog
	win_catalog()
	
	Example2
	from InjectA import win_catalog
	win_catalog(t1=20221001,t2=20221101)
	
	Example3
	see demos folder
	demos/test_43_win_catalog.py
	
	Example4
	counting TexNet catalog event number
	from InjectA import win_catalog
	lon1=-120;lon2=-90;lat1=20;lat2=50;t1=20160101;t2=20240101;
	win_catalog(t1=t1,t2=t2,lon_beg=lon1,lon_end=lon2,lat_beg=lat1,lat_end=lat2,foutcatalog='./tmp.txt')
	lon1=-104.7;lon2=-103.7;lat1=31.3;lat2=31.9;t1=20160101;t2=20240101;
	win_catalog(t1=t1,t2=t2,lon_beg=lon1,lon_end=lon2,lat_beg=lat1,lat_end=lat2,foutcatalog='./tmp.txt')
	
	lon1=-120;lon2=-90;lat1=20;lat2=50;t1=20220101;t2=20230101;
	win_catalog(t1=t1,t2=t2,lon_beg=lon1,lon_end=lon2,lat_beg=lat1,lat_end=lat2,foutcatalog='./tmp.txt')
	lon1=-104.7;lon2=-103.7;lat1=31.3;lat2=31.9;t1=20220101;t2=20230101;
	win_catalog(t1=t1,t2=t2,lon_beg=lon1,lon_end=lon2,lat_beg=lat1,lat_end=lat2,foutcatalog='./tmp.txt')
	'''

	from InjectA import create_catalog
	import obspy.core.utcdatetime as utc
	
	if fincatalog is None:
		fincatalog=os.getenv('HOME')+'/chenyk.data2/various/cyksmall/texnet_events_20240201.csv';

	f=open(fincatalog);
	lines=f.readlines();
	lines.pop(0) #or lines=lines[1:]
	lats=[float(ii.split(',')[6]) for ii in lines]
	lons=[float(ii.split(',')[8]) for ii in lines]
	deps=[float(ii.split(',')[10]) for ii in lines]
	eid0=[ii.split(',')[0] for ii in lines]
	utcs=[utc.UTCDateTime(ii.split(',')[2]+'T'+ii.split(',')[3]) for ii in lines]

	#Below is for standard time input
	if time_beg is None:
		time_beg=utc.UTCDateTime(2022, 10, 1, 00, 00, 00, 000000)
	if time_end is None:
		time_end=utc.UTCDateTime(2022, 11, 1, 00, 00, 00, 000000)

	#Below is for simple time input
	if t1 is None:
		pass
	else:
		t1=str(t1)
		if len(t1) != 8:
			TypeError("time_beg format error: 8 digits (e.g., 20221001)")
		else:
			year=int(t1[0:4])
			month=int(t1[4:6])
			day=int(t1[6:8])
			time_beg=utc.UTCDateTime(year, month, day, 00, 00, 00, 000000)

	if t2 is None:
		pass
	else:
		t2=str(t2)
		if len(t2) != 8:
			TypeError("time_end format error: 8 digits (e.g., 20221001)")
		else:
			year=int(t2[0:4])
			month=int(t2[4:6])
			day=int(t2[6:8])
			time_end=utc.UTCDateTime(year, month, day, 00, 00, 00, 000000)

	if lon_beg is None:
		lon_beg=-104.7;
	if lon_end is None:
		lon_end=-103.7;
	if lat_beg is None:
		lat_beg=31.3;
	if lat_end is None:
		lat_end=31.9;

	eids=[]
	for ii in range(len(lines)):
		if utcs[ii]>=time_beg and utcs[ii]<=time_end and lons[ii]>=lon_beg and lons[ii]<=lon_end and lats[ii]>=lat_beg and lats[ii]<=lat_end:
			eids.append(eid0[ii])
	print('Number of Catalog events in AOI is',len(eids))
	
	if foutcatalog is None:
		create_catalog(eids,fincatalog=fincatalog,foutcatalog='./texnet_events_%s_%s.csv'%(str(time_beg),str(time_end)));
	else:
		create_catalog(eids,fincatalog=fincatalog,foutcatalog=foutcatalog);
	

	return eids
	

	
	
	
	
	
	
	
	
	
	
	

