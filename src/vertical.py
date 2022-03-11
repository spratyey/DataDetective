from header import *
from sensor import Sensor_node


class Vertical:

    def __init__(self, uri, vertical_id, type):
        self.vertical_id = vertical_id
        self.uri = uri + str(vertical_id) + '/'
        self.type = type
        self.sensors = []
        print(self.uri)
        self.get_sensors()

    def get_sensors(self):
        response = requests.get(self.uri + '?rcn=4', headers=headers)
        jsondata = json.loads(response.text)
        # self.write_to_file(jsondata, "sample.json")
        sensorids = []
        for sensor in jsondata['m2m:ae']['m2m:cnt']:
            sensorids.append(sensor['rn'])
        for sensorid in sensorids:
            self.sensors.append(Sensor_node(server_uri, self.vertical_id, sensorid))
        return jsondata

    def write_to_file(self, jsondata, filename):
        json_object = json.dumps(jsondata, indent=4)
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)


vertical = Vertical(server_uri, 'AE-WE', 'weather')
