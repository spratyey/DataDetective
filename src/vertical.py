from header import *
from sensor import Sensor_node


class Vertical:

    def __init__(self, uri, vertical_id, type, opfile,config):
        self.vertical_id = vertical_id
        self.uri = uri + str(vertical_id) + '/'
        self.type = type
        self.sensors = []
        self.descriptors = []
        self.get_sensors(opfile,config)

    # def get_sensors(self, opfile):
    #     response = requests.get(self.uri + '?rcn=4', headers=headers)
    #     jsondata = json.loads(response.text)
    #     # self.write_to_file(jsondata, "sample.json")
    #     sensorids = []
    #     for sensor in jsondata['m2m:ae']['m2m:cnt']:
    #         sensorids.append(sensor['rn'])
    #     # print(self.uri,sensorids)
    #     for sensorid in sensorids:
    #         # print(self.uri, sensorid)
            
    #         self.sensors.append(Sensor_node(
    #             server_uri, self.vertical_id, sensorid, 'Data', opfile+sensorid+".txt"))
    #         break
    #         # self.descriptors.append(Sensor_node(
    #         #     server_uri, self.vertical_id, sensorid,'Descriptor'))
    #     return jsondata
    def get_sensors(self,opfile,config):
        for sensorid in config['sensor_nodes']:
            self.sensors.append(Sensor_node(
                server_uri, self.vertical_id, sensorid, 'Data', opfile+sensorid+".txt"))
            # self.descriptors.append(Sensor_node(
            #     server_uri, self.vertical_id, sensorid,'Descriptor'))
    def write_to_file(self, jsondata, filename):
        json_object = json.dumps(jsondata, indent=4)
        # Writing to sample.json
        with open(filename, "a") as outfile:
            outfile.write(json_object)




