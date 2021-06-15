### 第一部分：概念

1. future封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果（或抛出异常）后可以获取结果（或异常）。
2. Future对象：Future 类将可调用对象封装为异步执行。Future 实例由 Executor.submit() 创建。不应直接创建。


### 第二部分：比较依序执行和并发执行
1. 看下面的几个例子：  
   例子1 依序执行  
   例子2 使用concurrent.futures模块的Executor.map()  
   例子3 使用使用concurrent.futures模块的as_completed()和Executor.submit（）  
   例子4 使用asyncio包(见下章)  
   
2. 注意：例子1在单线程中运行。 
   例子2和3收到GIL限制都不能并行下载，任何时候只能运行一个线程，但是2和3依然比1快。

#### 例子1：下载完一个图像，并将其保存在硬盘中之后，才请求下载下一个图像
```
import os
import time
import sys
import requests
#要下载国旗图像的国家
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
#目标网站
BASE_URL = 'http://flupy.org/data/flags'

#保存目录
# DEST_DIR = 'downloads/'
DEST_DIR = '/Users/Huizhi/Downloads/'


def save_flag(img, filename):
    """保存图片"""
    path = os.path.join(DEST_DIR, filename) #获取图片保存的路径和名称
    with open(path, 'wb') as fp: #用二进制的方式将图片写到fp中，with释放资源
        fp.write(img)


def get_flg(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower()) #要下载的文件是http://www.flupy.org/data/flags/bd/bd.gif这种格式
    resp = requests.get(url) #requests 库中的 get() 方法能向服务器发送了一个请求，请求类型为 HTTP 协议的 GET 方式
    return resp.content #resp是响应，它是一个Response对象
    # Response.content	把数据转成二进制，用于获取图片、音频类的数据。
    #Response.text	把数据转为字符串，用于获取文本、网页原代码类的数据


def show(text):
    print(text, end=' ')
    sys.stdout.flush()
    #stdout具有缓冲区，不会每一次写入就输出内容，而是会在得到相应的指令后才将缓冲区的内容输出。
    #sys.stdout.flush()的作用就是显示地让缓冲区的内容输出。


def download_many(cc_list):
    #按照排序好的字符串下载
    for cc in sorted(cc_list):
        image = get_flg(cc) #返回二进制图片
        show(cc)  #在结果里告知，已经下载了哪些国家的
        save_flag(image, cc.lower() + '.gif') #存储图片
    return len(cc_list)


def main():
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()


"""
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN 
20 flags downloaded in 16.08s
"""

```

#### 例子2：使用concurrent.futures模块，同时请求下载所有图像，下载完一个文件就保存一个文件
1. 使用futures.ThreadPoolExecutor类实现多线程下载的脚本
2. 重点看download_many函数

```python

from concurrent import futures

import os
import sys
import time

import requests

#最大线程数
MAX_WORKERS = 10

# 要下载国旗图像的国家
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
# 目标网站
BASE_URL = 'http://flupy.org/data/flags'

# 保存目录
# DEST_DIR = 'downloads/'
DEST_DIR = '/Users/Huizhi/Downloads/'


def save_flag(img, filename):
    """保存图片"""
    path = os.path.join(DEST_DIR, filename)  # 获取图片保存的路径和名称
    with open(path, 'wb') as fp:  # 用二进制的方式将图片写到fp中，with释放资源
        fp.write(img)


def get_flg(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())  # 要下载的文件是http://www.flupy.org/data/flags/bd/bd.gif这种格式
    resp = requests.get(url)  # requests 库中的 get() 方法能向服务器发送了一个请求，请求类型为 HTTP 协议的 GET 方式
    return resp.content  # resp是响应，它是一个Response对象
    # Response.content	把数据转成二进制，用于获取图片、音频类的数据。
    # Response.text	把数据转为字符串，用于获取文本、网页原代码类的数据


def show(text):
    print(text, end=' ')
    sys.stdout.flush()
    # stdout具有缓冲区，不会每一次写入就输出内容，而是会在得到相应的指令后才将缓冲区的内容输出。
    # sys.stdout.flush()的作用就是显示地让缓冲区的内容输出。


def download_one(cc):
    image = get_flg(cc)  # 返回二进制图片
    show(cc)  # 在结果里告知，已经下载了哪些国家的
    save_flag(image, cc.lower() + '.gif')  # 存储图片
    return cc


def download_many(cc_list):
    # executor.shutdown(wait=True): 只有在所有待执行的 future 对象完成执行且释放已分配的资源后才会返回
    #这里用了with，所以会调用executor.__exit__，就不用再用 executor.shutsown函数了
    workers = min(MAX_WORKERS, len(cc_list)) #最大线程数
    with futures.ThreadPoolExecutor(workers) as executor:  #使用 ThreadPoolExecutor 来实例化线程池对象。传入workers参数来设置线程池中最多能同时运行的线程数目。
        res = executor.map(download_one, sorted(cc_list)) #map()是将序列中的每个元素都执行同一个函数
    return len(list(res))


def main():
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()

"""
TRRU  BD NG DE EG IN VN CN ID BR FR JP PH IR US ET CD MX PK 
20 flags downloaded in 1.12s
"""

```

#### 例子3：使用concurrent.futures模块，用executor.submit方法和futures.as_completed函数


```python

from concurrent import futures

import os
import sys
import time

import requests


# 要下载国旗图像的国家
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
# 目标网站
BASE_URL = 'http://flupy.org/data/flags'

# 保存目录
# DEST_DIR = 'downloads/'
DEST_DIR = '/Users/Huizhi/Downloads/'


def save_flag(img, filename):
    """保存图片"""
    path = os.path.join(DEST_DIR, filename)  # 获取图片保存的路径和名称
    with open(path, 'wb') as fp:  # 用二进制的方式将图片写到fp中，with释放资源
        fp.write(img)


def get_flg(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())  # 要下载的文件是http://www.flupy.org/data/flags/bd/bd.gif这种格式
    resp = requests.get(url)  # requests 库中的 get() 方法能向服务器发送了一个请求，请求类型为 HTTP 协议的 GET 方式
    return resp.content  # resp是响应，它是一个Response对象
    # Response.content	把数据转成二进制，用于获取图片、音频类的数据。
    # Response.text	把数据转为字符串，用于获取文本、网页原代码类的数据


def show(text):
    print(text, end=' ')
    sys.stdout.flush()
    # stdout具有缓冲区，不会每一次写入就输出内容，而是会在得到相应的指令后才将缓冲区的内容输出。
    # sys.stdout.flush()的作用就是显示地让缓冲区的内容输出。

def download_one(cc):
    image = get_flg(cc)  # 返回二进制图片
    show(cc)  # 在结果里告知，已经下载了哪些国家的
    save_flag(image, cc.lower() + '.gif')  # 存储图片
    return cc


def download_many(cc_list):
    # cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        to_do =[]
        #这个循环用submit创建Future对象
        for cc in sorted(cc_list):
            """
            使用 submit 函数来提交线程需要执行的任务（函数名和参数）到线程池中
            注意: submit() 不是阻塞的，而是立即返回。
            """
            task = executor.submit(download_one, cc)
            to_do.append(task)
            msg = 'Scheduled for {}:{}'
            print(msg.format(cc, task))
        results =[]
        ##这个循环用as_complated和result来获得结果
        for task in futures.as_completed(to_do):
            #as_completed() 方法是一个生成器，在没有任务完成的时候，会阻塞，
            # 在有某个任务完成的时候，会 yield这个任务，就能执行for循环下面的语句，然后继续阻塞住，循环到所有的任务结束
            res = task.result()  #使用 result() 方法可以获取任务的返回值，通常这个方法是阻塞的。但是在as_completed中是不堵塞的
            msg = '{} result: {!r}'
            print(msg.format(task, res))
            results.append(res)
        return len(results)



def main():
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()

"""
20 flags downloaded in 1.01s
"""

```

#### 例子4：使用asyncio包，同时请求下载所有图像，下载完一个文件就保存一个文件（见下章）





