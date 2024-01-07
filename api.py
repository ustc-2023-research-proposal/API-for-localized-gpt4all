"""
需要仿照OpenAI的格式给出具体的返回,以便于嵌套进入程序中,
而不对本身openai.st做相关的更改
openai给出的返回example:

{
  "data": [
    {
      "embedding": [
        -0.006929283495992422,
        -0.005336422007530928,
        ...
        -4.547132266452536e-05,
        -0.024047505110502243
      ],
      "index": 0,
      "object": "embedding"
    }
  ],
  "model": "text-embedding-ada-002",
  "object": "list",
  "usage": {
    "prompt_tokens": 5,
    "total_tokens": 5
  }
}

"""

from flask import Flask
from flask import request
import json
from gpt4all import GPT4All, Embed4All

embedder = Embed4All( model_name='all-MiniLM-L6-v2-f16.gguf')

# 建立embedder用于产生embed
app = Flask(__name__)

@app.route('/embed', methods=['get','post'])
def embedding():
	# 对输入进入的texts文本进行embedding处理
    

    data = request.get_json() # get_json会直接返回str而非json量

    input = data["input"]
    model = data["model"]

    return form_out(input,model)


# 暂时不清楚其中存不存在这种功能
@app.route('/moderation', methods=['get','post'])
def moderation():
    input = json.loads(request.form['input'])
    pass


def form_out(input, model) :
    data = []
    # 对传输进入的每一段文本都进行编号和embedding返回
    for index in range(len(input)):
        embed = embedder.embed(input[index])
        data.append({
            "embedding" : embed,
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
        "model" : model ,
        "object" : object ,
        "usage" : usage ,
    }

    return json.dumps(output)


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=6008)
