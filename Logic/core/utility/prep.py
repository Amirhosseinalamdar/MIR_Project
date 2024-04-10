import json

file_path = "./indexer/index/documents_index.json"

with open(file_path, "r") as json_file:
    data = json.load(json_file)


with open('./utility/eval_data.json', "r") as json_file:
    eval_data = json.load(json_file)

prep = {}
for q in eval_data:
    prep[q] = []
    for id in eval_data[q]:
        if id in data:
            prep[q].append(id)

file_path = './utility/prep_eval_data.json'
with open(file_path, "w") as json_file:
    json.dump(prep, json_file)