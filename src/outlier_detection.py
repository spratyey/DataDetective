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
import matplotlib as mpl

# to suppress a matplotlib memory runtime warning
mpl.rc('figure', max_open_warning=0)


def detect_outliers(dir_path, file_name, metadata_permission):
    """
    Detects outliers and generates the corresponding visualization plot for a given file.
    Args:
        dir_path: the path to the directory containing the file
        file_name: the name of the file to be analyzed
        metadata_permission: a boolean value indicating whether the metadata should be updated (redundant in the latest version of DataDetective, was used in the previous version when an 'interactive' mode existed)
    """
    with open(dir_path+'/'+file_name) as json_file:
        data = json.load(json_file)

    sensor_data = []
    
    if len(data['feeds'])>1: # if only one datapoint is posted, no point in doing outlier detection
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


        s_train = pd.DataFrame(sensor_data, index=None)
        s_train = s_train.set_index(0)
        s_train = s_train.fillna(0)
        s_train = validate_series(s_train)
        
        # detect outliers using the LocalOutlierFactor algorithm
        nneigh = min(len(data['feeds'])-1,20)
        outlier_detector = OutlierDetector(LocalOutlierFactor(contamination=0.05, n_neighbors=nneigh))
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



