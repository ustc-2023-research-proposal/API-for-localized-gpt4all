# 写在最前面
有一些想法,但还在尝试:
1. ollama本来是在`localhost:11434`上能够直接调用,那么为什么需要使用ngrok来映射到公网ip中?
  - 我的猜想是:整个向ollama请求的过程会不会是在convex上执行的,而不是在本地请求了之后上传至convex中?
    - 证明过程:
        1. 在Convex官方给出的doc中.![Alt text](https://docs.convex.dev/assets/images/TutorialFigure0-47bd164e06a7396ba005666938c5005b.png)因此我认为其架构方式是通过convex官方的服务器来调用`function`中的`action`去请求其他cloud服务,即`other cloud services`,那么自然也不可能直接调用到前端`frontend`的api.
        2. 在Convex的dashboard中可以找到其function目录,但是其中的一些函数是不能显示的`source code`,并且在更改`ai-town`本地文件时在其中会有一个上传的的过程.因此我认为这部分本地的代码可能上传到convex上运行的.
        3. ollama的端口需要经过ngrok来映射到公网ip,可能是因为convex不能直接调用服务器的本地端口,而需要存在转发过程,否则便不需要ngrok来多此一举了.
  - 另外则是当时尝试直接将`openai.ts`中的`openai`的url改成本地的`127.0.0.1:6008`时,本地的访问中并没有观察到相应的请求出现,可能是因为这个请求本身不是在本地执行的?而是在convex上执行的,因此本地的api从未收到任何请求.
  - 而openai.com不会受到影响,因为是公网ip,convex能够访问到?因此可以直接调用openai的api来进行embedding?
  - **因此现在的尝试方向是将api的本地端口使用ngrok映射到公网上,来看看能否正常接受到请求**
  - **已经成功了,看来必须将其放置于公网ip上才能访问到**
2. 向ollama的fetch请求频繁的错误
   - 我在convex的log上观察到的`aiTown/agentOperations:agentGenerateMessage`的错误?
     - `failure Uncaught SyntaxError: Unexpected token < in JSON at position 0`
     - 似乎是指出现了错误的 `<` 字符? 而这个字符不应该出现在json格式中,并且刚好出现在第0个位置

# 使用
1. 在python 3.12.1 与 python 3.11.0 中能够成功使用
2. 在使用前需要先安装 flask 与 gpt4all 的python库, 才可以使用
```
conda install flask
##################
使用gpt4all来进行embedding
pip install gpt4all
##################
如果是使用BAAI来进行embedding的话请使用`api-for-bge-large-en-v1.5.py`
目前在端口6009上运行,可以自行更改,同样需要使用代理
第一次使用会自动下载模型
pip install sentence-transformers
需要使用 python version <= 3.11 版本来安装 sentence-transformers
##################

```
等类似方法来进行安装.

# API
1. 将文件`git clone`到本地
2. 尽量在使用代理的情况来下来运行api文件,如果出现在`embedder = Embed4All( model_name='all-MiniLM-L6-v2-f16.gguf')`该行报错,可以尝试重启,会因为该原因在此处卡住
3. 如果没有model会在初次运行时自动下载(确保已经开启代理),如果出现
```
     File "/home/tenghao/API/api.py", line 6, in <module>
    embedder = Embed4All( model_name='all-MiniLM-L6-v2-f16.gguf')
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tenghao/miniconda3/envs/gpt4all/lib/python3.12/site-packages/gpt4all/gpt4all.py", line 44, in __init__
    self.gpt4all = GPT4All(model_name or 'all-MiniLM-L6-v2-f16.gguf', n_threads=n_threads, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
类似错误则尝试更换终端重新运行.

4. 成功界面会类似于:
```
bert_load_from_file: gguf version     = 2
bert_load_from_file: gguf alignment   = 32
bert_load_from_file: gguf data offset = 695552
bert_load_from_file: model name           = BERT
bert_load_from_file: model architecture   = bert
bert_load_from_file: model file type      = 1
bert_load_from_file: bert tokenizer vocab = 30522
 * Serving Flask app 'api'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:6008
 * Running on http://192.168.50.181:6008
Press CTRL+C to quit
 * Restarting with stat
bert_load_from_file: gguf version     = 2
bert_load_from_file: gguf alignment   = 32
bert_load_from_file: gguf data offset = 695552
bert_load_from_file: model name           = BERT
bert_load_from_file: model architecture   = bert
bert_load_from_file: model file type      = 1
bert_load_from_file: bert tokenizer vocab = 30522
 * Debugger is active!
 * Debugger PIN: 139-638-609
```
出现该界面则表示成功.(当然前面出现报错情况除外)

5. 每次请求后都会在下方显示请求
```
127.0.0.1 - - [21/Jan/2024 17:18:40] "POST /embed HTTP/1.1" 200 -
```
类似标识表示接收到请求

6. 当前api为仅能接收json格式的传输数据,因此不再能够直接使用`127.0.0.1:6008:embed?text=xxxx`的格式来进行输入了
7. 如果接收后但是没有正常返回,也可能是在请求过程中由于非法输入(鲁棒性很差,没有去检测非法输入)导致的api卡死,这点可以通过使用ctrl+c之后的返回结果来得到,如果发生错误会在ctrl+c后显示错误.
8. 测试请使用embed.py进行,运行embed.py程序,如果能够正常返回embedding的结果,并且能在api界面观察到`127.0.0.1 - - [21/Jan/2024 17:18:40] "POST /embed HTTP/1.1" 200 -`则表明正常访问(请求成功的status为200)

# embed.py
1. 在运行了api.py的前提下使用
2. 函数传入的为string的数组

而 Chat Completions的操作在gpt4all中存在该形式,只不过依然需要在 API 中编写响应的返回形式(gpt4all.doc)[https://docs.gpt4all.io/gpt4all_python.html#gpt4all.gpt4all.GPT4All.generate]

# !!!
**正在尝试使用docker来建立gpt4all镜像,其镜像的api编写完全按照openai官网提供的api来使用,便不需要使用gpt4all给python提供的函数重写api了**
