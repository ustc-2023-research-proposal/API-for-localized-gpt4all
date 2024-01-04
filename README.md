# api
api.py用于创建活动窗口
- 默认端口为6008
- 允许使用post和get方法进行调用
- 需要预先安装 gpt4all package
  -  若无法运行,可以尝试挂梯子,似乎gpt4all库会与openai进行连接
- 在python 3.12.1上能够成功运行
# embed
采用python
- embed内存在两个函数,分别以post和get方式来调用api
- 传入参数text便可
- 端口改变的话就改变url中的6008改为相应端口号
  - 没有判断错误输入,如果很久都没有响应的话建议关闭api重新运行
