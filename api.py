from flask import Flask
from flask import request
import json
from gpt4all import GPT4All, Embed4All

text = 'The quick brown fox jumps over the lazy dog'

embedder = Embed4All( model_name='all-MiniLM-L6-v2-f16.gguf')

app = Flask(__name__)

@app.route('/embed', methods=['get','post'])
def embedding():

    text = request.values.get('text')
    output = embedder.embed(text)
    json_str = json.dumps(output)
    return json_str


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=6008)