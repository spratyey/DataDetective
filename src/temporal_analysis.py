import datetime
import json
import numpy as np
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join


def freq_analysis(dirpath):
	
	files_in_dir = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

	for file in files_in_dir:
		
		with open(dirpath+"/"+file) as json_file:
			data = json.load(json_file)
			sensor_interval_list=[]
			for i in range(0,len(data['feeds'])-1):
				timestamp1 = data['feeds'][i]['created_at']
				timestamp2 = data['feeds'][i+1]['created_at']
				
				datetime_obj1 = datetime.datetime.strptime(
					timestamp1, '%Y-%m-%dT%H:%M:%S%z')
				datetime_obj2 = datetime.datetime.strptime(
					timestamp2, '%Y-%m-%dT%H:%M:%S%z')
				
				sensor_interval_list.append(datetime.timedelta.total_seconds(datetime_obj1-datetime_obj2))

			plt.plot(sensor_interval_list)
			plt.ylabel('Interval between readings (s)')
			plt.xlabel('Reading number (sorted chronologically)')
			plt.savefig(dirpath+"/analytics/freq_"+file.split('.')[0]+".png", dpi=100)
			plt.clf()


def nan_analysis(dirpath):

	files_in_dir = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

	for file in files_in_dir:

		with open(dirpath+"/"+file) as json_file:
			data = json.load(json_file)
			sensor_nan_list = []
			for i in range(0, len(data['feeds'])-1):
				nans=0
				for key in data['feeds'][i]:
					if type(data['feeds'][i][key]) == str:
						new_val = data['feeds'][i][key].replace(' ', '')
						if(new_val == 'nan'):
							nans+=1
				sensor_nan_list.append(nans)


			plt.plot(sensor_nan_list)
			plt.ylabel('Number of nan fields in a reading')
			plt.xlabel('Reading number (sorted chronologically)')
			plt.savefig(dirpath+"/analytics/nans_"+file.split('.')[0]+".png", dpi=100)
			plt.clf()

			
