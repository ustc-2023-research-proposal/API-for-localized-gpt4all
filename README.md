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

现在能够完成使用gpt4all进行embedding操作,并且为了**不直接修改openai.ts的代码**,因此**采用了和openAI API一样的返回格式**  
但是 Moderation 操作 并没有在 gpt4all的API中找到,似乎这是openai API中专门使用的功能  
即可能需要对源代码进行一定程度上的删减  

而 Chat Completions的操作在gpt4all中存在该形式,只不过依然需要在 API 中编写响应的返回形式(gpt4all.doc)[https://docs.gpt4all.io/gpt4all_python.html#gpt4all.gpt4all.GPT4All.generate]
