#!/usr/bin/python3
import colorama
from matplotlib.pyplot import close
from sensor import cache_sensor_data
from header import *
import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from iiith_api_functions import *
from logger import logthis
import sys
import getopt
from colorama import Fore, Back, Style
from alive_progress import alive_bar
import time
from temporal_analysis import freq_analysis


def read_verticals():
    """
    Reads the verticals from the config file.
    Calls the Sensor_node class in a nested manner to fully fetch and locally cache all data of sensor_nodes of all verticals.
    Args: 
        None
    Returns: 
        None
    """

    with open('verticalconfig.json') as json_file:

        # load config file data
        config_file_data = json.load(json_file)

        # for each vertical in the config file, ...
        for vertical in config_file_data['verticals']:
            print(vertical["vertical_id"])
            # ...make the corresponding local dir
            vert_dir = f'''./output/{vertical['vertical_id']}'''
            os.mkdir(vert_dir)


            # ... and for each sensor in the vertical, ...
            with alive_bar(len(vertical['sensor_nodes'])) as bar:
                for sensor_id in vertical['sensor_nodes']:
                    # ...fetch all data of the sensor
                    cache_sensor_data(sensor_id, vert_dir)
                    time.sleep(0.01)
                    bar()
                    
            pruned_nodes=0
            for sensor_id in vertical['sensor_nodes']:
            
                temp_f = open(vert_dir+'/'+sensor_id+'.json') 
                if len(temp_f.readlines())==0:
                    temp_f.close()
                    os.remove(vert_dir+'/'+sensor_id+'.json')
                    pruned_nodes+=1
            if pruned_nodes>0:
                print(f'''{pruned_nodes} nodes were pruned''')
            print("\n")
    # close the config file
    json_file.close()


def setup_api():

    function_status="Failure"

    # fetch the current api key from the env file
    api_key = os.getenv('API_KEY')
    status=0
    response="none"
    # check if the fetched key is still valid
    try:
        status, response = introspect_api_key(api_key)
        if status != 200:
            # if not valid, generate a new one
            print("Current API key is invalid. Generating New ...")

            # fetch the new key
            try:
                status,api_key = get_api_key(os.getenv('USER_EMAIL'),os.getenv('USER_PASSWORD'))
                if status != 200:
                    function_status="Failure"
                else:
                    # write the new key to the env file
                    update_environment(api_key)
                    function_status="Success"
            except:
                function_status="Failure"
        else:
            function_status="Success"
    except:
        function_status="Failure"

    

    return function_status


def main():
    interactive=False
    choice = '0'
    options, args = getopt.getopt(sys.argv[1:], 'hi123', ['help','interactive','fetch','freq','nan'])
    colorama.init()

    for opt,arg in options:
        if opt in ('-h', '--help'):
            choice = '0'
        elif opt in ('-i', '--interactive'):
            interactive=True
            choice = input(
                "Select task\n1. Fetch data and cache locally \n2. Time Intervals \n3. NaN detection\n")
        elif opt in ('-1','--fetch'):
            choice = '1'
        elif opt in ('-2','--freq'):
            choice = '2'
        elif opt in ('-3','--nan'):
            choice = '3'

    if choice == '0':
        print("Usage: datawarden [OPTIONs]...")
        print("Options:")
        print(" -h or --help: Print this help message")
        print(" -i or --interactive: Interactive mode")
        print(" -1 or --fetch: If not in interactive mode, fetch data and cache locally")
        print(" -2 or --freq: If not in interactive mode, perform posting frequency analytics")
        print(" -3 or --nan: If not in interactive mode, perform nan posting analytics")
        
    elif choice == '1':
        for i in range(25):
            func_status=setup_api()
            if func_status=="Success":
                break
            if i==24:
                logthis("API is likely down. Failed to fetch API key.")
                exit()
                
        
        if os.path.exists('./output'):
            shutil.rmtree('./output')
        os.mkdir("./output")
        read_verticals()

        
    elif choice == '2':
        if interactive:
            Tk().withdraw()
            dirpath = askdirectory()
            if os.path.exists(dirpath+"/analytics"):
                shutil.rmtree(dirpath+"/analytics")
            os.mkdir(dirpath+"/analytics")
            freq_analysis(dirpath)
    elif choice == '3':
        print("Performing nan posting analytics ...")
    else:
        print("Invalid choice. Use -h or --help for help")

main()
