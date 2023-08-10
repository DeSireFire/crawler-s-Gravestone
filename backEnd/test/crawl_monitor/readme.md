# 使用文档 - 监控信息推流客户端

这是一篇使用文档，介绍了基于Python的logging模块开发的日志推流程序，该程序用于将日志信息推送到监控平台，方便对日志进行集中管理和监控。

## 初始化参数说明

在使用该程序之前，需要实例化 `CrawlLogUper` 对象，并提供以下参数：

- `token` (必需): 监控平台的工作流密钥，用于识别和区分不同的项目或任务。
- `ip_address` (可选): 推送信息的服务端地址，默认为 "127.0.0.1"。
- `port` (可选): 推送信息的服务端端口，默认为 "50829"。
- `uper_name` (可选): 上传者名称，用于在监控平台标识不同的日志上传者。
- `up_switch` (可选): 布尔值，表示是否开启推送监控信息，True为开启，False为关闭，默认为True。

示例代码：
```
obj = CrawlLogUper(
    token="a158dc3a9d0f71283132f2c1127bc8c0",
    ip_address="127.0.0.1",
    port="50829",
    uper_name="测试上传者",
    up_switch=True
)
```

## 快速开始
```
from logClient import CrawlLogUper
obj = CrawlLogUper(
    token="a158dc3a9d0f71283132f2c1127bc8c0",
    uper_name="tester",
    up_switch=False
)
logger = obj.logger

# 根据需要，在你想的代码位置加入日志打印
logger.info(f'这是一条 信息 日志，发出来测试一下！！！')
logger.error(f'这是一条 错误 日志，发出来测试一下！！！')
logger.warning(f'这是一条 警告 日志，发出来测试一下！！！')

# 如果需要推送数据入库计数
# obj.items_total()

# 如果程序运行完或者需要手动关闭推送任务
# end_point()
```


## 方法介绍
0. 获取工作流密钥
密钥是开启监控推送的前提。
进入监控平台，依次进入
> 项目管理 > 项目列表 

根据情况创建或进入相应的项目
> (项目名称) > 工作流定义

根据情况，选中并查看密钥，或者创建工作流定义,查看密钥即可。
将密钥复制下来，留着。


1. logger
logger是日志记录器对象，用于记录日志信息。在实例化 CrawlLogUper 对象后，可通过 obj.logger 访问该对象。

示例代码：
```
logger = obj.logger
```

2. info(), error(), warning(), debug()
这些方法用于记录不同级别的日志信息，包括信息、错误、警告和调试等。
   
示例代码：
```
logger.info("这是一条信息日志")
logger.error("这是一条错误日志")
logger.warning("这是一条警告日志")
logger.debug("这是一条调试日志")
```

3. items_total(items_count)
items_total方法用于上传数据入库条数信息到监控平台。参数 items_count 为整数类型，表示要上传的数据入库条数。
   
示例代码：
```
obj.items_total(10)
```

4. end_point()
end_point方法用于在程序结束时执行的函数，通常用于执行一些清理操作或记录程序结束状态。

示例代码：
```
obj.end_point()
```

## 实例化使用

1. 首先，导入 CrawlLogUper 类。

```
from your_module import CrawlLogUper
```

2. 实例化 CrawlLogUper 对象，并提供必要的参数。

```
obj = CrawlLogUper(
    token="a158dc3a9d0f71283132f2c1127bc8c0",
    ip_address="127.0.0.1",
    port="50829",
    uper_name="测试上传者",
    up_switch=True
)
```

3. 通过 obj.logger 访问日志记录器对象，并使用 info(), error(), warning(), debug() 等方法记录不同级别的日志信息。

```
logger = obj.logger
logger.info("这是一条信息日志")
logger.error("这是一条错误日志")
logger.warning("这是一条警告日志")
logger.debug("这是一条调试日志")
```

4. 如果需要上传数据入库条数信息，使用 obj.items_total() 方法，传入入库条数。

```
# 例如：此处爬虫将有10条数据入库，所以这里写了10条。
# 不传值时，默认为1
obj.items_total(10)
```

5.在程序结束时，可以调用 obj.end_point() 方法执行一些清理操作。

```
obj.end_point()
```

## 注意事项
```
请确保监控平台的工作流密钥 token 正确并与监控平台保持一致，以便日志信息能够准确推送到对应的任务实例。

在实例化 CrawlLogUper 对象时，如果 up_switch 参数设置为 False，则不会推送监控信息，仅作为日志打印使用。

确保在程序结束时调用 obj.end_point() 方法，以便记录程序的结束状态。

以上便是该日志推流程序的使用文档，通过按照文档指引，您可以轻松使用该程序记录和推送日志信息至监控平台，

方便对日志进行集中管理和监控。

如有任何疑问或问题，请随时与我们联系。
祝您使用愉快！
```
