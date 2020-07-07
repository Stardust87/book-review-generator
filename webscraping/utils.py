import json

def save_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    
    return data