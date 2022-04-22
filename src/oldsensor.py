import os
from header import *
from iiith_api_functions import *
import datetime
api_key_temp=os.getenv('API_KEY')
class Sensor_node:
    def __init__(self, server_uri, vertical_id, node_id, data_type, opfile):
        self.node_id = node_id
        self.vertical_id = vertical_id
        self.uri = server_uri + vertical_id + \
            "/" + node_id + f'/{data_type}/?rcn=4'
        self.data = []
        self.descriptors = {}
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
    def parse_time(self):
        current_time = str(datetime.datetime.now())
        # delete after a .
        current_time = current_time[:current_time.find('.')]
        end_time_http = current_time.replace(
            ' ', 'T') + 'Z'
        start_time_http = current_time[:8] + str(int(current_time[8:10]) - 1) + current_time[10:]
        start_time_http = start_time_http.replace(
            ' ', 'T') + 'Z'
        return [start_time_http, end_time_http]
    def fetch_data(self, opfile):
        opf = open(opfile, 'a')
        # get current time
        time_range = self.parse_time()
        # print(time_range)
        # convert time to http TZ format
        
        # print(current_time_http)

        response = get_temporal_data(api_key_temp,self.node_id,time_range[0],time_range[1])
        if response == "No response":
            opf.write("No Data exists for this node")
        else:
            try:
                try:
                    response = json.loads(response)
                except:
                    # print("No Data exists for this node")
                    opf.write("No Data exists for this node")
                    return
                if 'feeds' in response:
                    for feed in response['feeds']:
                        data = []
                        for i in range(11):
                            if 'field' + str(i+1) in feed:
                                val = feed['field' + str(i+1)]
                                if val == '  nan':
                                    val = -12345.0
                                data.append(float(val))
                        self.data.append(data)
                else:
                    opf.write("No Data exists for this node")
                    return
                if 'channel' in response:
                    self.descriptors = response['channel']
            except:
                opf.write("No Data exists for this node")
                return

        # else:
        #     if 'm2m:cin' in jsondata['m2m:cnt'].keys():
        #         for i in range(len(jsondata['m2m:cnt']['m2m:cin'])):
        #             parsed_data = jsondata['m2m:cnt']['m2m:cin'][i]['con'][1:-1].split(
        #                 ', ')
        #             for j in range(len(parsed_data)):
        #                 try:
        #                     float_val = float(parsed_data[j])
        #                     if parsed_data[j] == 'nan':
        #                         float_val = -12345.0
        #                 except:
        #                     float_val = -12345.0
        #                 parsed_data[j] = float_val
        #             self.data.append(parsed_data)
        #             print(parsed_data)
        #     print(response.text)
        #     self.write_to_file(jsondata, 'sensor_data.json')
        # print(response)

    def write_to_file(self, jsondata, filename):
        json_object = json.dumps(jsondata, indent=4)
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)


# sensor = Sensor_node(server_uri, 'AE-WE', 'WE-VN04-00')
