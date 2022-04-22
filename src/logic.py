
from sensor import cache_sensor_data
from header import *
import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from iiith_api_functions import *
from logger import logthis


def read_verticals():
    """
    Reads the verticals from the config file.
    Calls the Sensor_node class in a nested manner to fully fetch and locally cache all data of sensor_nodes of all verticals.
    Args: 
        None
    Returns: 
        None
    """
    print("APIKEY: ",os.getenv('API_KEY'))

    with open('verticalconfig.json') as json_file:

        # load config file data
        config_file_data = json.load(json_file)

        # for each vertical in the config file, ...
        for vertical in config_file_data['verticals']:

            
            # ...make the corresponding local dir
            vert_dir = f'''./output/{vertical['vertical_id']}'''
            os.mkdir(vert_dir)

            # ... and for each sensor in the vertical, ...
            for sensor_id in vertical['sensor_nodes']:

                # ...fetch all data of the sensor
                cache_sensor_data(sensor_id, vert_dir)

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
    choice = input(
        "Select task\n1. Fetch data and cache locally \n2. Time Intervals \n3. NaN detection\n")
    if choice == '1':

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

main()
