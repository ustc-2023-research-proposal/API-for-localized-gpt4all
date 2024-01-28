# 实验结果
最近的在那个[task-and-result.md](https://github.com/ustc-2023-research-proposal/API-for-localized-gpt4all/blob/main/task-and-result.md)里面
~~有一些想法,但还在尝试:~~  
正在写一从convex中读取数据的程序,希望能以更加整洁合适的表格形式来呈现对话内容,并且将对话结果存储在本地下以便得出实验结论.  

## API转发至公网IP下 & Ollama转发至公网IP下
1. ollama本来是在`localhost:11434`上能够直接调用,那么为什么需要使用ngrok来映射到公网ip中?
  - **必须将其放置于公网ip上才能访问到**
  - 我的猜想是:整个向ollama请求的过程会不会是在convex上执行的,而不是在本地请求了之后上传至convex中?
    - 证明过程:
        1. 在Convex官方给出的doc中.![Alt text](https://docs.convex.dev/assets/images/TutorialFigure0-47bd164e06a7396ba005666938c5005b.png)因此我认为其架构方式是通过convex官方的服务器来调用`function`中的`action`去请求其他cloud服务,即`other cloud services`,那么自然也不可能直接调用到前端`frontend`的api.
        2. 在Convex的dashboard中可以找到其function目录,但是其中的一些函数是不能显示的`source code`,并且在更改`ai-town`本地文件时在其中会有一个上传的的过程.因此我认为这部分本地的代码可能上传到convex上运行的.
        3. ollama的端口需要经过ngrok来映射到公网ip,可能是因为convex不能直接调用服务器的本地端口,而需要存在转发过程,否则便不需要ngrok来多此一举了.
  - 另外则是当时尝试直接将`openai.ts`中的`openai`的url改成本地的`127.0.0.1:6008`时,本地的访问中并没有观察到相应的请求出现,可能是因为这个请求本身不是在本地执行的?而是在convex上执行的,因此本地的api从未收到任何请求.
  - 而openai.com不会受到影响,因为是公网ip,convex能够访问到?因此可以直接调用openai的api来进行embedding?

## Memory
1. 目前已经能够完成一轮对话,并且产生对应的memory,计算出相应的embedding结果与importance的值
2. 从头至尾没有使用过`OPENAI_API_KEY`,但是这个变量需要存在,但可以随意赋值,如`OPENAI_API_KEY is too expensive`,否则会无法运行

# Ollama运行一段时间后会请求错误
1. 向ollama的fetch请求频繁的错误
   - **目前情况下,在ai-town运行约15分钟左右后便始终处于`fetch fail`的状态,目前具体情况不明**
   - 我在convex的log上观察到的`aiTown/agentOperations:agentGenerateMessage`的错误?
     - `failure Uncaught SyntaxError: Unexpected token < in JSON at position 0`
     - 似乎是指出现了错误的 `<` 字符? 而这个字符不应该出现在json格式中,并且刚好出现在第0个位置

# 关于ngrok只能转发一个端口的解决方案
1. 首先可以找一个熟悉的同学,然后一个人转发ollama的端口,一个人转发api的端口,两者都能够使用.
2. 或者可以选择在本地装一个tmole然后将端口从服务器上转发到本地,再从本地转发到公网ip上(可以不使用ngrok)
  1. 首先在本地电脑(区别于服务器)中安装nodejs
  2. 使用nodejs安装tunnlemole
  3. 输入`tmole <本地端口号>`来讲本地端口转发到公网上
  4. 使用如ssh等(我使用的是vscode的remote ssh插件)转发服务器端口到本地端口
    - 这边需要转发至少一个端口到本地(ollama 或 api 端口),也可以都使用tmole而不使用ngrok
    - 使用`3`将端口号转发到公网ip上
  5. 更新在convex中的环境变量
    - 这里可以将比如78行处的openai网址改为环境变量`process.env.API_URL`,然后直接在convex的dashboard中更改`API_URL`环境变量即可
    - 建议设置一个`embedding vector length`的的变量用于快捷修改embedding后的长度
  7. convex需要有一个上传函数的过程,如果觉得源代码未上传,可以在更改后的代码界面尝试保存更改,应该会自动更新

# embedding嵌入中产生的错误
  1. 如果出现了 **行数不匹配** 的原因,需要修改`convex/agent/schema.ts`目录下43行处`dimensions: 1536,`的大小
    - 这里是在检测api返回的embedding维度的大小,这边默认是1536,即openai的embedding的向量大小,将其改为api对应的模型的对应向量长度
    - 这边给出可能使用到的大小
      - BAAI:1024
      - gpt4all:384

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
3. 如果需要测试,也可以使用
4. 

# 在openai.ts中的代码更改
将78,79行中,将代码改为
```
    const openaiApiBase = process.env.OPENAI_API_BASE || '转发到公网的api端口(注意最后不能有'/')';
    const apiUrl = openaiApiBase + '/embed';
```
将84行注销掉

最后的结果应当如下所示:
```Javascript {.line-numbers}
export async function fetchEmbeddingBatch(texts: string[]) {
    assertOpenAIKey();
  const {
    result: json,
    retries,
    ms,
  } = await retryWithBackoff(async () => {
    const openaiApiBase = process.env.OPENAI_API_BASE || '转发到公网的api端口(注意最后不能有'/')'; // <----- 此处,或者采用环境变量的方式来改变亦可
    const apiUrl = openaiApiBase + '/embed';   // <----- 此处
    const result = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Authorization: 'Bearer ' + process.env.OPENAI_API_KEY,   // <----- 此处
      },

      body: JSON.stringify({
        model: 'text-embedding-ada-002',
        input: texts.map((text) => text.replace(/\n/g, ' ')),
      }),
    });
    if (!result.ok) {
      throw {
        retry: result.status === 429 || result.status >= 500,
        error: new Error(`Embedding failed with code ${result.status}: ${await result.text()}`),
      };
    }
    return (await result.json()) as CreateEmbeddingResponse;
  });
  if (json.data.length !== texts.length) {
    console.error(json);
    throw new Error('Unexpected number of embeddings');
  }
  const allembeddings = json.data;
  allembeddings.sort((a, b) => a.index - b.index);
  return {
    embeddings: allembeddings.map(({ embedding }) => embedding),
    usage: json.usage.total_tokens,
    retries,
    ms,
  };
}
``` 
