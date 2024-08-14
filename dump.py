import requests
import json

es_url = "http://localhost:9200"


def dump(index):
    print(f"dumping index {index}")
    page_size = 100
    page_index = 0
    while True:
        match_all = f'{{ "from": {page_index*page_size}, "size": {page_size}, "query": {{ "match_all": {{}} }} }}'
        request_url = f"{es_url}/{index}/_search"
        result = requests.post(request_url, data=match_all, headers={'Content-Type': 'application/json'}).json()
        hits = result['hits']['hits']
        final_result = [hit['_source'] for hit in hits]
        if len(final_result) == 0:
            break
        # save these
        with open(index, 'a', encoding="utf-8") as file:
            for hit in final_result:
                file.write(f"{json.dumps(hit)}\n" )
        
        page_index += 1
        print(f"page = {page_index}")

indicies = ["seasons", "products", "sku", "collection_mapping", "category"]
for index in indicies:
    dump(index)
