import os, zipfile, json

def create_zip(path, dest, opt):
    files = os.listdir(path)
    with zipfile.ZipFile(dest, opt, allowZip64=True) as archive:
        for file in files:
            archive.write(os.path.join(path, file), file)

def add_to_zip(path, dest, opt):
    with zipfile.ZipFile(dest, opt, allowZip64=True) as archive:
        archive.write(path, os.path.basename(path))
        
def unzip_file(path, dest):
    with zipfile.ZipFile(path, 'r') as archive:
        archive.extractall(dest)

def read_print_json(path, pretty, sort):
	with open(path) as file:
		data = json.load(file)
		print(json.dumps(data, sort_keys=sort, indent=4 if pretty else data))

def update_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
        
def update_json_attr(path, key, value):
    with open(path, 'r') as file:
        data = json.load(file)
        data[key] = value
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

def main():
    read_print_json('./test_folder/test.json', True, True)
    update_json_attr('./test_folder/test.json', 'name', 'test')
    read_print_json('./test_folder/test.json', True, True)


main()