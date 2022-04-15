import matplotlib
from iiith_api_functions import get_api_key, introspect_api_key
from vertical import Vertical
from sensor import Sensor_node
from header import *
import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from matplotlib import pyplot as plt
import numpy as np
from operator import itemgetter
from pathlib import Path

def read_verticals():
	# load config file
	with open('verticalconfig.json') as json_file:
		data = json.load(json_file)
		verticals = {}
		for vertical in data['verticals']:
			verticals.update({
				vertical['vertical_id']: Vertical(
				    server_uri, vertical['vertical_id'], vertical['type'])
			})

		return verticals


def analysis(fpath, choice):
	fi = open(fpath, 'r')
	raw_readings=eval(fi.read())

	if len(raw_readings)==0:
		print("Subscription node. No data.")
		return

	readings = sorted(raw_readings, key=itemgetter(0))
	readings.sort()

	if not os.path.exists(os.path.dirname(fpath)+"/analytics"):
		os.mkdir((os.path.dirname(fpath))+"/analytics")
	
	if choice == "2":
		intervals_analysis(readings, fpath)
	else :
		nan_analysis(readings, fpath)

def intervals_analysis(readings, fpath):
	interval_list=[]
	for i in range (0, len(readings)-1):
		interval_list.append(float(readings[i+1][0])-float(readings[i][0]))

	plt.plot(interval_list)
	plt.ylabel('Interval between readings (s)')
	plt.xlabel('Reading number (sorted chronologically)')
	plt.savefig((os.path.dirname(fpath))+"/analytics/"+Path(fpath).stem+"_intervals.png", dpi=100)
	plt.show()
	


def nan_analysis(readings, fpath):
	print("in nan analysis")
	nannum=np.zeros(len(readings))
	for i in range (0, len(readings)):
		for datapoint in readings[i]:
			if datapoint==-12345.0:
				nannum[i]+=1

	plt.plot(nannum)
	plt.ylabel('Number of NaN values per reading')
	plt.xlabel('Reading instance number (sorted chronologically)')
	plt.savefig((os.path.dirname(fpath))+"/analytics/"+Path(fpath).stem+"_nan.png", dpi=100)
	plt.show()

	
def read_verticals(config_file):
	# load config file
	with open(config_file) as json_file:
		data = json.load(json_file)
		print(data)
		return data

	



def main():
	vert_config = read_verticals('verticalconfig.json')
	api_key = os.getenv('API_KEY')
	if introspect_api_key(api_key) != 200:
		print("Invalid API key. Generating New....")
		api_key = get_api_key(os.getenv('USER_EMAIL'), os.getenv('USER_PASSWORD'))
	update_environment(api_key)
	verticals = []
	choice=input("Select task\n1. Fetch OneM2M data into files \n2. Time Intervals \n3. NaN detection\n")
	if choice=='1':
		shutil.rmtree('./output')

		os.mkdir("./output")
		for vertical in vert_config['verticals']:
			os.mkdir(f'''./output/{vertical['vertical_id']}''')
			# os.mkdir(f'''./output/em''')
			# os.mkdir(f'''./output/sl''')
			# os.mkdir(f'''./output/aq''')
			verticals.append(Vertical(server_uri, f'''AE-{vertical['vertical_id']}''', 'weather', f"./output/{vertical['vertical_id']}/",vertical))
		 
		# vertical = Vertical(server_uri, 'AE-WE', 'weather', "./output/we/")
		# vertical2= Vertical(server_uri, 'AE-EM', 'energy', "./output/em/")
		# vertical3= Vertical(server_uri, 'AE-SL', 'solar', "./output/sl/")
		# vertical4= Vertical(server_uri, 'AE-AQ', 'airquality', "./output/aq/")
		
	
		
	elif choice=='2' or choice=='3':
		Tk().withdraw()  
		filename = askopenfilename() 
		analysis(filename, choice)

		
		
main()