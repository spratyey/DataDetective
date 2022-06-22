import datetime
import json
import numpy as np
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join


def freq_analysis(dirpath, metadata_permission):
	"""
	Performs frequency analysis on a vertical.
	Args:
		dirpath: the path to the directory containing the vertical's sensors
		metadata_permission: whether or not to write metadata to file
	"""	
	files_in_dir = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

	for file in files_in_dir:
		
		with open(dirpath+"/"+file) as json_file:
			data = json.load(json_file)
			sensor_interval_list=[]
			max_gap=0
			if len(data['feeds'])>1: # if just one datapoint, why do freq analysis at all
				for i in range(0,len(data['feeds'])-1):
					timestamp1 = data['feeds'][i]['created_at']
					timestamp2 = data['feeds'][i+1]['created_at']
					
					# find the 'gap lengths' between two consecutive datapoints
					datetime_obj1 = datetime.datetime.strptime(
						timestamp1, '%Y-%m-%dT%H:%M:%S%z')
					datetime_obj2 = datetime.datetime.strptime(
						timestamp2, '%Y-%m-%dT%H:%M:%S%z')
					diff = datetime.timedelta.total_seconds(datetime_obj1-datetime_obj2)
					sensor_interval_list.append(diff)
					max_gap = max(max_gap, diff)

				plt.plot(sensor_interval_list)
				plt.ylabel('Interval between readings (s)')
				plt.xlabel('Reading number (sorted chronologically)')
				plt.savefig(dirpath+"/analytics/freq_"+file.split('.')[0]+".png", dpi=100)
				plt.clf()

				if metadata_permission:
					metadata=[]
					if isfile("./output/metadata/freq_metadata.json"):
						with open("./output/metadata/freq_metadata.json") as f:
							metadata = json.loads(f.read())
					metadata.append({"node": file.split('.')[0], "max_gap": max_gap})
					with open("./output/metadata/freq_metadata.json","w") as f:
						json.dump(metadata, f, indent=4, separators=(',', ': '))



def nan_analysis(dirpath, metadata_permission):
	"""
	Performs nan analysis on a vertical.
	Args:
		dirpath: the path to the directory containing the vertical's sensors
		metadata_permission: whether or not to write metadata to file
	"""
	files_in_dir = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

	for file in files_in_dir:

		with open(dirpath+"/"+file) as json_file:
			data = json.load(json_file)
			sensor_nan_list = []
			total_nans=0
			num_values=0 #readings*fields
			nan_params=set()
			for i in range(0, len(data['feeds'])):
				nans=0
				for key in data['feeds'][i]:
					num_values+=1
					if type(data['feeds'][i][key]) == str:
						new_val = data['feeds'][i][key].replace(' ', '')
						if(new_val == 'nan'):
							nans+=1
							nan_params.add(data['channel'][key])
				sensor_nan_list.append(nans)
				total_nans+=nans
				


			plt.plot(sensor_nan_list)
			plt.ylabel('Number of nan fields in a reading')
			plt.xlabel('Reading number (sorted chronologically)')
			plt.savefig(dirpath+"/analytics/nans_"+file.split('.')[0]+".png", dpi=100)
			plt.clf()

			if metadata_permission:
				metadata = []
				if isfile("./output/metadata/nans_metadata.json"):
					with open("./output/metadata/nans_metadata.json") as f:
						metadata = json.loads(f.read())
				metadata.append({"node": file.split('.')[0], "nan_percent": total_nans/num_values, "nan_params": list(nan_params)})
				with open("./output/metadata/nans_metadata.json", "w") as f:
					json.dump(metadata, f, indent=4, separators=(',', ': '))

			
