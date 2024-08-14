import requests
import json

es_url = "http://localhost:9200"


def import_data(index, index_name):
    print(f"importing index {index} ")
    buffer_size = 100
    buffer = []
    page_index = 0
    with open(index, encoding="utf-8") as file:
        while True:
            line = file.readline()
            if len(line) > 0:
                buffer.append(line)
            else:
                break
            if len(buffer) == buffer_size:
                print(f"index the buffer {page_index}")
                page_index += 1
                index_data(buffer[:], index_name)
                buffer = []
                
        
    if len(buffer) > 0:
        print(f"index the the remaining buffer {len(buffer)}")
        index_data(buffer[:], index_name)

def index_data(data, index_name):
    print(f"indexing {index_name}")
    new_data = []
    for element in data:
        element_json = json.loads(element)
        new_data.append({ "index": { "_id": element_json["id"] } })
        del element_json['score']
        new_data.append(element_json)
    request_url = f"{es_url}/{index_name}/_bulk"
    bulk_request = ""
    for element in new_data:
        bulk_request += f"{json.dumps(element)}\n"
    requests.post(request_url, data=bulk_request, headers={'Content-Type': 'application/json'})

indicies = ["seasons", "products", "sku", "collection_mapping", "category"]

for index in indicies:
    import_data(index, f"{index}")
