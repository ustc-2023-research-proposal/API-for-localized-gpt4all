import requests
import json

def getEmbedding(text:str) :

    url = 'http://127.0.0.1:6008/embed?' +'text=' + text
    r = requests.get(url=url, verify=False)
    return json.loads(r.text)

def PostEmbedding(text:str) :
    url = 'http://127.0.0.1:6008/embed'
    data = {'text' : text}
    r = requests.post(url=url, data=data)
    return json.loads(r.text)

print(getEmbedding('Hey? How are you?'))

print(PostEmbedding('maybe?'))
