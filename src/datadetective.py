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
from notification import daily_summary
from temporal_analysis import freq_analysis, nan_analysis
from outlier_detection import outlier_analysis
from os.path import isfile, join

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def perform_daily_analysis():

    # fetching
    for i in range(25):
        func_status = setup_api()
        if func_status == "Success":
            break
        if i == 24:
            logthis("API is likely down. Failed to fetch API key.")
            exit()


    if os.path.exists('./output'):
        shutil.rmtree('./output')
    os.mkdir("./output")
    
    if os.path.exists('./output/metadata'):
        shutil.rmtree('./output/metadata')
    os.mkdir("./output/metadata")
    
    
    read_verticals()

    # perform the analysis
    print("Data Posting Frequency Analysis")
    perform_freq_analysis(False)
    print("NaN Value Analysis")
    perform_nan_analysis(False)
    print("Outlier Analysis")
    perform_outlier_analysis(False)
    daily_summary('./output/metadata')

def perform_outlier_analysis(interactive):
    if interactive:
        Tk().withdraw()
        dirpath = askdirectory()
        outlier_analysis(dirpath, False)
    else:
        if isfile("./output/metadata/outlier_metadata.json"):
            os.remove("./output/metadata/outlier_metadata.json")
        with open('verticalconfig.json') as json_file:

            # load config file data
            config_file_data = json.load(json_file)
            with alive_bar(len(config_file_data['verticals'])) as bar:
                # for each vertical in the config file, ...
                for vertical in config_file_data['verticals']:
                    outlier_analysis("output/"+vertical["vertical_id"], True)
                    time.sleep(0.01)
                    bar()

def perform_freq_analysis(interactive):

    
    if interactive:
        Tk().withdraw()
        dirpath = askdirectory()
        freq_analysis(dirpath, False)
    else:

        if isfile("./output/metadata/freq_metadata.json"):
            os.remove("./output/metadata/freq_metadata.json")

        with open('verticalconfig.json') as json_file:

            # load config file data
            config_file_data = json.load(json_file)
            with alive_bar(len(config_file_data['verticals'])) as bar:
                # for each vertical in the config file, ...
                for vertical in config_file_data['verticals']:
                    freq_analysis("output/"+vertical["vertical_id"], True)
                    time.sleep(0.01)
                    bar()


def perform_nan_analysis(interactive):


    if interactive:
        Tk().withdraw()
        dirpath = askdirectory()
        nan_analysis(dirpath, False)
    else:
        if isfile("./output/metadata/nans_metadata.json"):
            os.remove("./output/metadata/nans_metadata.json")

        with open('verticalconfig.json') as json_file:

            # load config file data
            config_file_data = json.load(json_file)
            with alive_bar(len(config_file_data['verticals'])) as bar:
                # for each vertical in the config file, ...
                for vertical in config_file_data['verticals']:
                    nan_analysis("output/"+vertical["vertical_id"], True)
                    time.sleep(0.01)
                    bar()

            

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
            os.mkdir(vert_dir+"/analytics")


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
    options, args = getopt.getopt(sys.argv[1:], 'hi123456', ['help','interactive','fetch','freq','nan','outlier','notif','daily'])


    for opt,arg in options:
        if opt in ('-h', '--help'):
            choice = '0'
        elif opt in ('-i', '--interactive'):
            interactive=True
            choice = input(
                "Select task\n1. Fetch data and cache locally \n2. Time Intervals / Frequency Analysis \n3. NaN detection\n4. Outlier detection\n")
        elif opt in ('-1','--fetch'):
            choice = '1'
        elif opt in ('-2','--freq'):
            choice = '2'
        elif opt in ('-3','--nan'):
            choice = '3'
        elif opt in ('-4','--outlier'):
            choice = '4'
        elif opt in ('-5','--notif'):
            choice = '5'
        elif opt in ('-6','--daily'):
            choice = '6'

    if choice == '0':
        print("Usage: datawarden [OPTIONs]...")
        print("Options:")
        print(" -h or --help: Print this help message")
        print(" -i or --interactive: Interactive mode")
        print(" -1 or --fetch: If not in interactive mode, fetch data and cache locally")
        print(" -2 or --freq: If not in interactive mode, perform posting frequency analytics")
        print(" -3 or --nan: If not in interactive mode, perform nan posting analytics")
        print(" -4 or --outlier: If not in interactive mode, perform outlier/anomaly analytics")
        print(" -5 or --notif: If not in interactive mode, perform notification analytics")
        print(" -6 or --daily: If not in interactive mode, perform full daily posting routine")
        
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

        if os.path.exists('./output/metadata'):
            shutil.rmtree('./output/metadata')
        os.mkdir("./output/metadata")
        
        read_verticals()

        
    elif choice == '2':
        perform_freq_analysis(interactive)
    elif choice == '3':
        perform_nan_analysis(interactive)
    elif choice == '4':
        perform_outlier_analysis(interactive)
    elif choice == '5':
        daily_summary('./output/metadata')
    elif choice == '6':
        perform_daily_analysis()
    else:
        print("Invalid choice. Use -h or --help for help")

main()
