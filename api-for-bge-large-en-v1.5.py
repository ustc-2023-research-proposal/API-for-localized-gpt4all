from flask import Flask
from flask import request
import json
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('BAAI/bge-large-en-v1.5')

# 建立embedder用于产生embed
app = Flask(__name__)

@app.route('/embed', methods=['get','post'])
def embedding():
	# 对输入进入的texts文本进行embedding处理
    

    data = request.get_json() # get_json会直接返回str而非json量

    input = data["input"]
    model = data["model"]

    return form_out(input,model)


def form_out(input, model_name) :
    # 对传输进入的每一段文本都进行编号和embedding返回

    data = []
    embeddings = model.encode(input, normalize_embeddings=True).tolist()

    for index in range(len(embeddings)):
        data.append({
            "embedding" : embeddings[index],
            "index" : index,
            "object" : "embedding"
        })
    
	# 这个指代这次调用API消耗的tokens量,由于不用openai的api后随意设置
    usage = {
        "prompt_tokens": 0,
        "total_tokens": 0,
    }
    
    object = "list"

    output = {
        "data" : data ,
        "model" : model_name ,
        "object" : object ,
        "usage" : usage ,
    }
    print(output)
    return json.dumps(output)


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=6009)
