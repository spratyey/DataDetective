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

    def get_sensors(self,opfile,config):
        for sensorid in config['sensor_nodes']:
            self.sensors.append(Sensor_node(
                server_uri, self.vertical_id, sensorid, 'Data', opfile+sensorid+".txt"))
            



