import json

with open('fnn_crawler/data/tinhte/tinhte_corpus_post_8.json') as json_file:
    data = json.load(json_file)
    print(len(data))
    # json_file.write(']')

# import os
# print(os.path.basename('fnn_crawler/data/voz/voz_informal_text3.json'))