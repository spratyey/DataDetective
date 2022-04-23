import datetime
import json
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
from adtk.data import validate_series
from adtk.visualization import plot
from adtk.detector import QuantileAD, OutlierDetector
from sklearn.neighbors import LocalOutlierFactor

# datestring for which datetime_obj required


def detect_outliers(dir_path, file_name, metadata_permission):
    with open(dir_path+'/'+file_name) as json_file:
        data = json.load(json_file)

    sensor_data = []
    for feeds in data['feeds']:
        date_string = feeds['created_at']
       
        datetime_obj = datetime.datetime.strptime(
            date_string, '%Y-%m-%dT%H:%M:%S%z')
        cin = []
        cin.append(datetime_obj)
        for key in feeds:
            if type(feeds[key]) == float or type(feeds[key]) == int:
                cin.append(feeds[key])
            elif type(feeds[key]) == str:
                new_val = feeds[key].replace(' ', '')
                if(new_val == 'nan'):
                    cin.append(np.nan)
        sensor_data.append(cin)

    # print(sensor_data[0])

    s_train = pd.DataFrame(sensor_data, index=None)
    s_train = s_train.set_index(0)
    s_train = s_train.fillna(0)
    s_train = validate_series(s_train)
    # print(s_train)
    outlier_detector = OutlierDetector(LocalOutlierFactor(contamination=0.05))
    anomalies = outlier_detector.fit_detect(s_train)
    plot(s_train, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_color='red',
         anomaly_alpha=0.3, curve_group='all', save_to_file=dir_path+"/analytics/outlier_"+file_name.split('.')[0]+".png")


    
   
    if metadata_permission:

        anomalies = anomalies.tolist()
        num_anom=0
        for i in range(len(anomalies)):
            if anomalies[i]==True:
                num_anom+=1
        metadata = []
        if isfile("./output/metadata/outlier_metadata.json"):
            with open("./output/metadata/outlier_metadata.json") as f:
                metadata = json.loads(f.read())
        metadata.append({"node": file_name.split('.')[0], "num_anomalies": num_anom})
        with open("./output/metadata/outlier_metadata.json", "w") as f:
            json.dump(metadata, f, indent=4, separators=(',', ': '))

def outlier_analysis(dirpath, metadata_permission):
    files_in_dir = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    for file in files_in_dir:
        detect_outliers(dirpath, file, metadata_permission)



