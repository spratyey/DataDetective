import os
from urllib import response
from header import *
from iiith_api_functions import *
from datetime import datetime, timedelta
from logger import logthis
import time



def cache_sensor_data (sensor_id, vert_dir):
    """
    Fetches data and caches it in the given directory.
    As in read_verticals(), a maximum of 25 API call attempts are made per sensor.
    Args:
        sensor_id: the sensor id of the sensor whose data is to be fetched
        vert_dir: the directory in which the data is to be cached
    Returns:
        None
    """
    for i in range(25):
        permission_to_log = i>20 # Due to the inherent unreliability of the API, each sensor requires 7-8 calls to actually get data (provided the data exists in the first place). Hence, we only start logging after the first 20 (out of 25) attempts are made.
        func_status,data = fetch_data(sensor_id, permission_to_log)
        if func_status == "Success":
            break
        time.sleep(0.1)
        if(i==24):
            logthis("Error in fetching data for sensor_id: "+sensor_id)
    write_to_file(data, vert_dir+'/'+sensor_id+'.json')



def fetch_data(sensor_id, permission_to_log):
    """
    Fetches data from the API and returns it to the caller.
    Args:
        sensor_id: the sensor id of the sensor whose data is to be fetched
        permission_to_log: a boolean indicating whether the function should log the API call failure.
    Returns:
        func_status: a string indicating the status of the function
        data: the data returned by the API
    """
    function_status="Failure"

    # get time interval
    start_time=""
    end_time=""
    data=""

    try:
        start_time, end_time = __get_time_interval()

        # fetch data by performing an API call
        api_key = os.getenv('API_KEY')

        response = get_temporal_data(api_key, sensor_id, start_time, end_time)
        if response=="No response":
            function_status="Failure"
        elif 'channel' in response :
            function_status="Success"
            data = response
        else:
            if permission_to_log:
                logthis("Error in fetching data for sensor_id: "+sensor_id+"\n"+response)
            function_status="Failure"
    except:
        function_status="Failure"
    return function_status, data



def write_to_file(data, filename):
    # Writing to sample.json
    with open(filename, "w") as outfile:
        outfile.write(data)


def __get_time_interval():

    # get datetime in ISO8601, and offset it by 5:30 [to compensate for the API's internal offset]
    end_time = str((datetime.now()+timedelta(hours=5)+timedelta(minutes=30)).isoformat(timespec='seconds'))+'Z'

    # start_time is 1 day before end_time
    start_time = str((datetime.now() +timedelta(hours=5)+timedelta(minutes=30)- timedelta(days=1)).isoformat(timespec='seconds'))+'Z'

    return start_time, end_time

