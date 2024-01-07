import requests
import json

def PostEmbedding(texts) :
    url = 'http://127.0.0.1:6008/embed'

    data = {
        'input' : texts,
        'model' : 'hello',
    }

    # 需要加入,在header中声明是以json形式来传输数据的
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    return r.text

if __name__ == '__main__':
    
    print(PostEmbedding(['hello','how are you']))
