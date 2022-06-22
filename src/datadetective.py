#!/usr/bin/python3

# This is the entry point for all of datadetective. Specifically, the line that calls the main method.

# imports
from sensor import cache_sensor_data
from header import *
import os
import shutil
from iiith_api_functions import *
from logger import logthis
import sys
import getopt
from alive_progress import alive_bar
import time
from notification import daily_summary
from temporal_analysis import freq_analysis, nan_analysis
from outlier_detection import outlier_analysis
from os.path import isfile


def perform_daily_analysis():
    """
    The full deal, all at once.
    Fetch, analyse, and send notifications.
    Args:
        None
    Returns:
        None
    """
    read_verticals()
    print("Data Posting Frequency Analysis")
    perform_freq_analysis()
    print("NaN Value Analysis")
    perform_nan_analysis()
    print("Outlier Analysis")
    perform_outlier_analysis()
    daily_summary()


def perform_outlier_analysis():
    """
    Performs outlier analysis on all the verticals.
    Calls the outlier detection framework ADTK, via the outlier_analysis function in outlier_detection.py.
    Args:
        None
    Returns:
        None
    """

    # get rid of previous metadata
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


def perform_freq_analysis():
    """
    Performs frequency analysis on all the verticals.
    Calls the freq_analysis function in temporal_analysis.py to perform frequency analysis.
    Args:
        None
    Returns:
        None
    """
    # get rid of previous metadata
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


def perform_nan_analysis():
    """
    Performs nan analysis on all the verticals.
    Calls the nan_analysis function in temporal_analysis.py to perform nan analysis.
    Args:
        None
    Returns:
        None
    """
    # get rid of previous metadata
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
    Reads the verticals as specified the config file.
    We first set up the API, then refresh the local caching directory setup, and then fetch data as per verticalconfig.json.
    Due to the unreliability of the API, we will try to fetch the data again and again if it fails, with a current hardcoded hard-cutoff at 25 attempts. 
    Post these 25 attempts, the node is considered 'dead'. It is added to the list of dead nodes, and its corresponding directory is pruned from the cache setup. 
    Args: 
        None
    Returns: 
        None
    """

    # set up the API
    for i in range(25):
        func_status = setup_api()
        if func_status == "Success":
            break
        if i == 24:
            logthis("API is likely down. Failed to fetch API key.")
            exit()

    # flush and refresh the output/cache directory setup
    if os.path.exists('./output'):
        shutil.rmtree('./output')
    os.mkdir("./output")
    if os.path.exists('./output/metadata'):
        shutil.rmtree('./output/metadata')
    os.mkdir("./output/metadata")

    with open('verticalconfig.json') as json_file:

        # load config file data
        config_file_data = json.load(json_file)
        for vertical in config_file_data['verticals']:
            print(vertical["vertical_id"])

            # for each vertical, make the corresponding local dir
            vert_dir = f'''./output/{vertical['vertical_id']}'''
            os.makedirs(vert_dir, exist_ok=True)
            os.makedirs(vert_dir+"/analytics", exist_ok=True)

            # fetch data for each sensor in the vertical
            with alive_bar(len(vertical['sensor_nodes'])) as bar:
                for sensor_id in vertical['sensor_nodes']:
                    cache_sensor_data(sensor_id, vert_dir)
                    time.sleep(0.01)
                    bar()

            # examine the corresponding files for each node to check for dead nodes       
            pruned_nodes=0
            for sensor_id in vertical['sensor_nodes']:
                temp_f = open(vert_dir+'/'+sensor_id+'.json') 
                if len(temp_f.readlines())==0: # if node is dead...
                    metadata = []
                    if isfile("./output/metadata/dead_nodes.json"):
                        with open("./output/metadata/dead_nodes.json") as f:
                            metadata = json.loads(f.read())
                    metadata.append({"Vertical": vertical["vertical_id"], "Node":sensor_id})
                    with open("./output/metadata/dead_nodes.json", "w") as f:
                        json.dump(metadata, f, indent=4, separators=(',', ': '))
                    temp_f.close()
                    os.remove(vert_dir+'/'+sensor_id+'.json')
                    pruned_nodes+=1
            if pruned_nodes>0:
                print(f'''{pruned_nodes} nodes were pruned''')
            print("\n")
    
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
        function_status="Failure" # yes there's probably more elegant ways to do this than three nested try-catches
    
    return function_status


def main():
    """
    Main function.
    Deals with command line args and dispatches to the appropriate function.
    Args:
        None
    Returns:
        None
    """
    choice = '0'
    options, args = getopt.getopt(sys.argv[1:], 'h123456', [
                                  'help', 'fetch', 'freq', 'nan', 'outlier', 'notif', 'daily'])

    for opt, arg in options:
        if opt in ('-h', '--help'):
            choice = '0'
        elif opt in ('-1', '--fetch'):
            choice = '1'
        elif opt in ('-2', '--freq'):
            choice = '2'
        elif opt in ('-3', '--nan'):
            choice = '3'
        elif opt in ('-4', '--outlier'):
            choice = '4'
        elif opt in ('-5', '--notif'):
            choice = '5'
        elif opt in ('-6', '--daily'):
            choice = '6'

    if choice == '0':
        print("Usage: datadetective [OPTIONs]...")
        print("Options:")
        print(" -h or --help: Print this help message")
        print(" -1 or --fetch: Fetch data and cache locally")
        print(" -2 or --freq: Perform posting frequency analytics")
        print(" -3 or --nan: Perform nan posting analytics")
        print(" -4 or --outlier: Perform outlier/anomaly analytics")
        print(" -5 or --notif: Perform notification analytics")
        print(" -6 or --daily: Perform full daily posting routine")

    elif choice == '1':
        read_verticals()
    elif choice == '2':
        perform_freq_analysis()
    elif choice == '3':
        perform_nan_analysis()
    elif choice == '4':
        perform_outlier_analysis()
    elif choice == '5':
        daily_summary()
    elif choice == '6':
        perform_daily_analysis()
    

# The precise entry point for all of datadetective
main()
