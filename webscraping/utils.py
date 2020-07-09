import json
import glob

def save_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def get_downloaded_user_ids(path):
    filenames = [ f.split('\\')[-1] for f in glob.glob(path)]
    user_ids = [ int(f.split('_')[-1].split('.')[0]) for f in filenames ]
    return user_ids

if __name__ == '__main__':
    get_downloaded_user_ids(r'.\data\users\*')