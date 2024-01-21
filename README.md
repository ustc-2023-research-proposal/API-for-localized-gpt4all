# 写在最前面
有一些想法,但还在尝试:
1. ollama本来是在`localhost:11434`上能够直接调用,那么为什么需要使用ngrok来映射到公网ip中?
  - 我的猜想是:整个向ollama请求的过程会不会是在convex上执行的,而不是在本地请求了之后上传至convex中?
  - 另外则是当时尝试直接将`openai.ts`中的`openai`的url改成本地的`127.0.0.1:6008`时,本地的访问中并没有观察到相应的请求出现,可能是因为这个请求本身不是在本地执行的?而是在convex上执行的,因此本地的api从未收到任何请求.
  - 而openai.com不会受到影响,因为是公网ip,convex能够访问到?因此可以直接调用openai的api来进行embedding?
  - **因此现在的尝试方向是将api的本地端口使用ngrok映射到公网上,来看看能否正常接受到请求**
2. 向ollama的fetch请求频繁的错误
   - 我在convex的log上观察到的`aiTown/agentOperations:agentGenerateMessage`的错误?
     - `failure Uncaught SyntaxError: Unexpected token < in JSON at position 0`
     - 似乎是指出现了错误的 `<` 字符? 而这个字符不应该出现在json格式中,并且刚好出现在第0个位置
# !!!
**正在尝试使用docker来建立gpt4all镜像,其镜像的api编写完全按照openai官网提供的api来使用,便不需要使用gpt4all给python提供的函数重写api了**
# API的创建
1. 将api.py文件clone到本地
2. 打开一个终端,并且需要在该终端上挂上梯子
   - gpt4all库需要与openai网络连接,否则可能会上不去
3. 默认调用端口号为127.0.0.1:6008
   - 可以在下方自行更改
4. 删除了get方式(因为似乎有安全隐患),现在只允许使用post方式来进行访问
5. 以header的形式声明传入的需要为json格式
6. 获取texts,即**string的数组**来进行响应

# embed.py
1. 在运行了api.py的前提下使用
2. 函数传入的为string的数组

# others
从openai.ts的源码中发现,其中**不止只调用了openAI_API来embedding操作**  
其中还包括 [Chat Completions](https://platform.openai.com/docs/guides/text-generation/chat-completions-api)   的调用,
以及 [moderation](https://platform.openai.com/docs/guides/moderation/moderation) 的调用, 判断当前文本的道德程度?(是否有违禁词之类的)
意味着其**仍然是使用openAI API来生成文本**的,但确实不清楚是在哪一方面使用该文本  

~现在能够完成使用gpt4all进行embedding操作,并且为了**不直接修改openai.ts的代码**,因此**采用了和openAI API一样的返回格式**~  
~但是 Moderation 操作 并没有在 gpt4all的API中找到,似乎这是openai API中专门使用的功能~  
即可能需要对源代码进行一定程度上的删减  

而 Chat Completions的操作在gpt4all中存在该形式,只不过依然需要在 API 中编写响应的返回形式(gpt4all.doc)[https://docs.gpt4all.io/gpt4all_python.html#gpt4all.gpt4all.GPT4All.generate]
