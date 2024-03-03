
import json


def del_snippet(category, name, path):
    with open(path + category + ".json", 'r') as f:
        data = json.load(f)
        # flatten list to dict
        # snippet_dict = {key: value for s in data for key, value in s.items()}
        for s in data.keys():
            if s == name:
                snip_delete = s
    del data[snip_delete]
    # open file and write data with key removed
    with open(path + category + ".json", 'w') as f:
        json.dump(data, f, indent=4)

path = "snippets/"
category = "docker"
name = "docker list all containers"
del_snippet(category, name, path)
