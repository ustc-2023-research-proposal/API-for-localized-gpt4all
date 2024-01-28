# 本次任务
## ollama错误原因?
### [OllamaLogs](https://github.com/ollama/ollama/blob/main/docs/troubleshooting.md)
给出了ollama的具体日志调用.以及错误查询方式

> On Linux systems with systemd, the logs can be found with this command:
```
journalctl -u ollama
```
的执行结果为:
```
Hint: You are currently not seeing messages from other users and the system.
      Users in groups 'adm', 'systemd-journal' can see all messages.
      Pass -q to turn off this notice.
-- No entries --
```
因此暂时没有办法使用.

### 在ollama的GitHub issues界面中寻找
- [在20个请求后挂起,重启后可以使用](https://github.com/ollama/ollama/issues/1910#issuecomment-1891057901)
- [请求json格式后可能会导致挂起](https://github.com/ollama/ollama/issues/1910#issue-2075323326)
- [ollama在30分钟运行后会挂起](https://github.com/ollama/ollama/issues/1458)
    - [小批量运行的很好,大批量容易停止](https://github.com/ollama/ollama/issues/1458#issuecomment-1860694325)
    - [在重新启动之前不会正常处理请求](https://github.com/ollama/ollama/issues/1458#issuecomment-18832410130)
- [json格式问题](https://github.com/ollama/ollama/issues/1135)
    - >I tried with v0.1.18 and for every --format json request it doesn't stop. After printing the JSON it continues to print empty lines forever. Because it never stops printing empty lines, it is as if it hangs forever.Does the JSON format model know when to stop? What stop words should I use? I tried stop="\n\n\n" without success.
- [几个小时后，Ollama 实例卡住并挂起](https://github.com/ollama/ollama/issues/2176)

### 总结
1. 大批量并且多次请求以及json格式的返回都有可能造成ollama的实例挂起
2. json格式的无限输出空行可能是导致ollama挂起的原因
3. 假如不以json格式返回则能够长时间运行?

### 子目标
1. 观察对ollama的请求是否是要求以json格式返回的?
    - 能否将其json格式改为一般格式,在从一般格式返回值?
    - 在[openai.ts](https://github.com/a16z-infra/ai-town/blob/c04dc0a3d2fb9f4c8e4713281e3d38599e5371c7/convex/util/openai.ts#L55)是将chatCompletion的结果作为json来进行解读(虽然认为这是openai的,但是ollama有一个对应的chatCompletion)
2. 如果是以json格式不能更改,则需要寻找ollama为何json格式的接收容易导致挂起
3. 在fetch中返回的错误信息? 
    - `fetch fail`的运行结果似乎是由于实例挂起.没有办法使用
    - `failure Uncaught SyntaxError: Unexpected token < in JSON at position 0`
    - 以及在运行过程中存在的warning,提示输入格式并非完全的json格式.

### 可能的解决方案
1. 使用非json格式返回?
2. 给ai-town的请求时间延长
3. 调查ai-town的输入格式问题
    - 探讨在向ollama输入后的json格式的形式的问题?

## Convex的内容导出
[导出convex快照](https://docs.convex.dev/database/import-export/export)

该方法能够顺利导出jsonl文件.

可以通过pandas将其转换为表格形式,并将playerID发生的messages整理成一个表格形式来进行参考

## Dialogue
在文本框中出现了多个对话.

目前我这边没有出现过类似的问题

## ai-town的运行时间
使用`ACTION_TIMEOUT`来设置的是允许model运行更多的时间以得到返回结果,即出现在convex的环境变量中.
其出现于convex目录下constant.ts的[53行](https://github.com/a16z-infra/ai-town/blob/c04dc0a3d2fb9f4c8e4713281e3d38599e5371c7/convex/constants.ts#L53)
```JavaScript
// Timeout a request to the conversation layer after a minute.
export function ACTION_TIMEOUT() {
  return Number(process.env.ACTION_TIMEOUT) || 60 * 1000;
}
```
- `IDLE_WORLD_TIMEOUT`是指一旦闲置五分钟以上,则其`inactivate engine`(?).
- `MAX_STEP`存在,是指最多的运行限制(?).

### 结论
暂时不确定这个`MAX_STEP`与`IDLE_WORLD_TIMEOUT`有什么作用,但按照[Running the simulation](https://github.com/a16z-infra/ai-town/blob/main/ARCHITECTURE.md#running-the-simulation)中的结果应该是可以发现其有:

> 2.Decide how long to run.

的说法,也就是说应该是存在这个运行次数限制的.