#  refmar.py
#  This module contains funtions to retrieve and process data from the 
#  REFMAR network of tide-gauge in France. It should be used with TAPPy
#
# 
#  Copyright 2015 Romarine <contact@romarine.org>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
  
#!/usr/bin/python3.4
# -*-coding:Latin-1 -*

import datetime
import requests
import json
	
# This function retrieve data from the REFMAR servers for a given period and write it in a JSON file
def get_observations(station=3,data_type=4,start_date='2014/12/30',end_date='2014/12/31'):
	
	#formatting date
	start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
	end_date = datetime.datetime.strptime(end_date, '%Y/%m/%d')
	
	# Server URL's for accessing REFMAR data
	url = 'http://services.data.shom.fr/sos/client'
	local_filename = 'station_'+str(station)+'_'+'Data_Type_'+str(data_type)+'_'+start_date.strftime('%Y-%m-%dT%H:%M:%SZ')\
	+'_'+end_date.strftime('%Y-%m-%dT%H:%M:%SZ')+'.json'

	# Creating the payload
	payload = {
		'request': 'GetObservation',
		'service': 'SOS',
		'version': '2.0.0',
		'procedure': ['http://shom.fr/maregraphie/procedure/'+str(station)],
		'offering': ['http://shom.fr/maregraphie/offering/'+str(station)],
		'observedProperty': ['http://shom.fr/maregraphie/observedProperty/WaterHeight/'+str(data_type)],
		'temporalFilter': [{'during': {'ref': 'om:phenomenonTime','value': [start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),end_date.strftime('%Y-%m-%dT%H:%M:%SZ')]}}],
		'responseFormat':['application/json']
           }
	#Header for the POST request
	headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

	#Request
#	r = requests.post(url,data = json.dumps(payload), headers=headers,stream=True)

#	with open(local_filename, 'wb') as f:
#		for chunk in r.iter_content(chunk_size=1024): 
#			if chunk: # filter out keep-alive new chunks
#				f.write(chunk)
#				f.flush()
	r = requests.post(url,data = json.dumps(payload), headers=headers)
	jsondata = r.json()
	
	with open(local_filename, 'wt') as f:
		for values in jsondata["data"]:
			print(values["timestamp"]," ",values['value'])
			f.write(values["timestamp"] + " " + str(values['value'])+"\n")
						
	return local_filename
