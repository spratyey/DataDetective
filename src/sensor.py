from header import *


class Sensor_node:
    def __init__(self, server_uri, vertical_id, node_id, data_type, opfile):
        self.node_id = node_id
        self.vertical_id = vertical_id
        self.uri = server_uri + vertical_id + \
            "/" + node_id + f'/{data_type}/?rcn=4'
        self.data = []
        if data_type == 'Data':
            self.fetch_data(opfile)
        elif data_type == 'Descriptor':
            self.fetch_descriptor()
        # print(server_uri)
        # print(self.uri)
        opf = open(opfile, 'w')
        opf.write(str(self.data))

    def fetch_descriptor(self):
        response = requests.get(self.uri, headers=headers)
        if response.status_code != 200:
            print("No Data exists for this node")
        else:
            jsondata = json.loads(response.text)
            print(response.text)
            self.write_to_file(jsondata, 'sensor_data.json')
        # print(response)

    def fetch_data(self, opfile):
        opf = open(opfile, 'a')
        response = requests.get(self.uri, headers=headers)
        if response.status_code != 200:
            opf.write("No Data exists for this node")
        else:
            jsondata = json.loads(response.text)
            if 'm2m:cin' in jsondata['m2m:cnt'].keys():
                for i in range(len(jsondata['m2m:cnt']['m2m:cin'])):
                    parsed_data = jsondata['m2m:cnt']['m2m:cin'][i]['con'][1:-1].split(
                        ', ')
                    for j in range(len(parsed_data)):
                        try:
                            float_val = float(parsed_data[j])
                            if parsed_data[j] == 'nan':
                                float_val = -12345.0
                        except:
                            float_val = -12345.0
                        parsed_data[j] = float_val
                    self.data.append(parsed_data)
                    # print(parsed_data)
            # print(response.text)
            # self.write_to_file(jsondata, 'sensor_data.json')
        # print(response)

    def write_to_file(self, jsondata, filename):
        json_object = json.dumps(jsondata, indent=4)
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)


# sensor = Sensor_node(server_uri, 'AE-WE', 'WE-VN04-00')
