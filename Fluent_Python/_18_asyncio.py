"""

asyncio.Future类与concurrent.futures.Future类之间的区别
第17章中下载国旗那些示例的异步版
摒弃线程或进程，如何使用异步编程管理网络应用中的高并发
在异步编程中，与回调相比，协程显著提升性能的方式
如何把阻塞的操作交给线程池处理，从而避免阻塞事件循环
使用asyncio编写服务器，重新审视Web应用对高并发的处理方式
为什么asyncio已经准备好对Python生态系统产生重大影响
"""
#第一部分：通过多线程程序和对应的asyncio版程序，说明多线程和异步任务之间的关系
#例子1：通过线程以动画形式显示文本式旋转指针
"""
import threading
import itertools
import time


def spin(msg, done):  # 
    for char in itertools.cycle('|/-\\'):  # itertools 为高效循环而创建迭代器的函数，有count(),cycle(),repeat()等等
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        if done.wait(.1):  # wait(timeout=None)：阻塞线程直到内部变量为 true 。
            # 当提供了timeout参数且不是 None 时，它应该是一个浮点数，代表操作的超时时间，以秒为单位（可以为小数）。
            break
    print(' ' * len(status), end='\r')

def slow_function():
    #假设这是耗时的计算
    # pretend waiting a long time for I/O
    time.sleep(5)  #调用sleep函数会阻塞主线程，不过一定要这么做，以便释放GIL，创建从属线程。
    #怎么理解GIL：在多核CPU调度多个线程任务。线程1在CPU1上执行，如果线程2想在CPU2上执行，得先等待CPU1的线程1释放GIL
    #GIL什么时候可能被释放：例如I/O阻塞或者time.sleep
    return 42


def supervisor():
    """
    #threading模块提供Event类实现线程之间的通信：一个线程发出事件信号，而其他线程等待该信号。
#线程通过wait()方法进入等待状态，直到另一个线程调用set()方法将内置标志设置为True时，Event通知所有等待状态的线程恢复运行

    """
    done = threading.Event() #相当于一个flag
    spinner = threading.Thread(target=spin,
                               args=('thinking!', done)) #创建从属线程对象
    print('spinner object:', spinner)  # 显示从属线程对象。输出类似于<Thread(Thread-1, initial)>。
    spinner.start()  # 启动从属线程活动
    result = slow_function()  #slow_functin会被阻塞运行5秒，也就是说从属线程会打印出5秒的'/\|thinking'
    #也就是说spin里面的wait会等待5秒
    done.set()  # 调用set()方法将内置标志设置为True时
    spinner.join()  # 等待至线程终止
    return result


def main():
    # main里面的是主线程，先调用supervisor（）
    #创建Event对象和spinner从属线程，启动从属线程（但是从属线程并不能运行，没有GIL还在主线程那里）
    #然后运行slow_function函数，阻塞主线程，释放GIL，同时，从属线程以动画形式显示旋转指针
    #等线程终止，返回result
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()
"""
#例子2：使用@asyncio.coroutine装饰器，以动画形式显示文本式旋转指针

import asyncio
import itertools


async def spin(msg):
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        try:
            await asyncio.sleep(.1)  #
        except asyncio.CancelledError:  # <3>
            break
    print(' ' * len(status), end='\r')


async def slow_function():  # <4>
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)  # <5>
    return 42


async def supervisor():  # <6>
    spinner = asyncio.create_task(spin('thinking!'))  # <7>
    print('spinner object:', spinner)  # <8>
    result = await slow_function()  # <9>
    spinner.cancel()  # <10>
    return result


def main():
    result = asyncio.run(supervisor())  # 驱动supervisor协程，让它运行完毕；这个协程的返回值是这次调用的返回值。
    print('Answer:', result)


if __name__ == '__main__':
    main()