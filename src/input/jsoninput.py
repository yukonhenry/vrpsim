''' Copyright YukonTR 2015 '''
__author__ = 'henry'
import simplejson as json
def read_json(json_filename, key):
    with open(json_filename) as json_file:
        json_data = json.load(json_file)
        info_list = json_data[key]
    return info_list
