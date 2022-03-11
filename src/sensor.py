from header import *


class Sensor_node:
    def __init__(self, server_uri, vertical_id, node_id):
        self.node_id = node_id
        self.vertical_id = vertical_id
        self.uri = server_uri + vertical_id + '/' + node_id + '/Data/la'
        self.data = []
        self.descriptor = {}
        self.fetch_data()
        print(self.uri)

    def fetch_data(self):
        response = requests.get(self.uri, headers=headers)
        jsondata = json.loads(response.text)
        print(jsondata)
        # print(response.text)

    def write_to_file(self, jsondata, filename):
        json_object = json.dumps(jsondata, indent=4)
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)


sensor = Sensor_node(server_uri, 'AE-WE', 'WE-VN04-00')
