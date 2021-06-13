### 第五部分：yield from 新句法的用途和语义：把职责委托给子生成器

```python
def gen():
    yield from subgen()
```

1. 主要功能：打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样二者可以直接发送产出值  
2. yield from是await的意思
3. 在生成器中使用yield from subgen()时，subgen会获得控制权，把产出的值传给gen的调用方
4. 与此同时，gen会阻塞，等待subgen终止

#### 例子1： 简单的yield from的例子

```python
def chains(*iterables):
    for it in iterables:
        yield from it  # yield from it 表示调用iter(it)，从中获取迭代器

s = 'abc'
t = tuple(range(3))
print(list(chains(s,t)))
#-->['a', 'b', 'c', 0, 1, 2]

```

#### 一些概念区分
1. 委派生成器：包含yield from <iterable> 表达式的生成器函数
2. 子生成器：从yield from表达式中<iterable>部分获取的生成器
3. 调用方：指调用委派生成器的客户端代码

#### 怎么工作：
1. 委派生成器在yield from 表达式处暂停时，调用方可以直接把数据发给子生成器
2. 子生成器再把产出的值给调用方  
3. 子生成器返回之后，解释器会抛出StopIteration异常，并把返回值附加到异常对象上，此时委派生成器会恢复

#### 例子2：使用yield from 计算平均值并输出统计报告
```python
from collections import namedtuple
Result = namedtuple('Result', 'count average')

#子生成器

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield  #main函数中的data直接发送到term
        if term is None: #终止条件，相应的，调用方最后也应该发送一个None过来
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average) #Result会成为grouper函数中yield from表达式的值。


#委派生成器
#这个循环每次迭代时会新建一个averager实例；每个实例都是作为协程使用的生成器对象。
def grouper(results, key):
    while True:     #子生成器收到None之后，解释器会抛出StopIteration异常，会返回Result，并在这里赋值给result[key]，没有收到None就不会赋值。
        #如果调用的方法抛出StopIteration异常，那么委派生成器恢复运行
        results[key] = yield from averager() #委派生成器在yield from暂停时，调用方可以直接将数据发给子生成器，子生成器再把产出的值发给调用方

        print(results)
        #{'girls;kg': Result(count=10, average=42.040000000000006)}
        # {'girls;kg': Result(count=10, average=42.040000000000006), 'girls;m': Result(count=10, average=1.4279999999999997)}
        # {'girls;kg': Result(count=10, average=42.040000000000006), 'girls;m': Result(count=10, average=1.4279999999999997), 'boys;kg': Result(count=9, average=40.422222222222224)}
        # {'girls;kg': Result(count=10, average=42.040000000000006), 'girls;m': Result(count=10, average=1.4279999999999997), 'boys;kg': Result(count=9, average=40.422222222222224), 'boys;m': Result(count=9, average=1.3888888888888888)}



#调用方
def main(data):
    results = {}
    for key, values in data.items(): #外层for循环创建委派生成器实例
        group = grouper(results, key) #group是生成器对象，group是委派生成器，作为协程使用。results用于收集结果。
        next(group)  #预激委派生成器grouper，此时进入while True循环，调用子生成器averager后，在yield from表达式处暂停
        for value in values: #内层for循环把值传给子生成器averager。
            group.send(value)#这个循环结束了之后result[key]赋值语句还没有执行。因此要送进去一个None
        group.send(None) #如果子生成器不终止，委派生成器会在yieldfrom表达式处永远暂停。子生成器停止，result[key]赋值
    report(results)

    # print(results)
    #{'girls;kg': Result(count=10, average=42.040000000000006),
    # 'girls;m': Result(count=10, average=1.4279999999999997),
    # 'boys;kg': Result(count=9, average=40.422222222222224),
    # 'boys;m': Result(count=9, average=1.3888888888888888)}



#    输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
              result.count, group, result.average, unit))



data = {
    'girls;kg':[40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m' :[1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg' :[39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m'  :[1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],

}


if __name__ == '__main__':
    main(data)
```

### 第六部分：使用协程管理仿真系统中的并发活动



1. 单个线程中使用一个主循环驱动协程执行并发活动。  
2. 使用协程做面向事件编程时，协程会不断把控制权让步给主循环，激活并向前运行其他协程，从而执行各个并发活动。属于协作式多任务。
3. 协作式多任务与抢占式多任务的区别：协作式环境下，下一个进程被调度的前提是当前进程主动放弃时间片；抢占式环境下，操作系统完全决定进程调度方案，操作系统可以剥夺耗时长的进程的时间片，提供给其它进程。（例如根据优先级）
4. 也就是协程和多线程的区别：协程显式自主地把控制权让步给中央调度程序。而多线程实现的是抢占式多任务。
调度程序可以在任何时刻暂停线程（即使在执行一个语句的过程中），把控制权让给其他线程。

#### 例子3：出租车拉客，用协程taxi_process实现各辆出租车的活动

```python


import collections
"""
定义事件，有三个参数
time: 事件发生时的仿真时间
proc: 出租车进程实例的编号
actions: 描述活动的字符串
"""
Event = collections.namedtuple('Event', 'time proc action')  #定义事件

def taxi_process(ident, trips, start_time = 0):  #每辆出租车都调用taxi_process函数，创建一个生成器对象
    """
    每次改变状态时创建事件，把控制权让给仿真器
    start_time: 出租车离开车库的时间
    time:事件发生的时间，例如乘客上下车的时间
    ident: 出租车的编号
    trips：出租车回家之前的行程数量

    """
    """#遇到yield Event时，总是会先生成Event再挂起。直到协程收到了发给它的time，然后运行到下一个yield Event，重复"""

    time = yield Event(start_time, ident, 'leave garage') #协程会暂停
    

    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')

    yield Event(time, ident, 'going home')



#用console驱动taxt_process协程
"""
>>> from _16_coroutine_2 import taxi_process
>>> taxi = taxi_process(ident=13, trips=2, start_time=0)
>>> next(taxi)
Event(time=0, proc=13, action='leave garage')
>>> taxi.send(_.time + 7)   #一定要在console里运行，不然会出现错误NameError: name '_' is not defined
Event(time=7, proc=13, action='pick up passenger')
>>> taxi.send(_.time + 23)
Event(time=30, proc=13, action='drop off passenger')
>>> taxi.send(_.time + 5)
Event(time=35, proc=13, action='pick up passenger')
>>> taxi.send(_.time + 48)
Event(time=83, proc=13, action='drop off passenger')
>>> taxi.send(_.time + 1)
Event(time=84, proc=13, action='going home')
>>> taxi.send(_.time + 10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>>
"""

#把上面在console写的写在仿真类Simulator里面
import queue
import random
import collections
import argparse

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

class Simulator:

    def __init__(self, procs_map):
        """
        1. PriorityQueue对象，保存Event 实例。有put和get两个方法
        2. 优先队列的好处：创建事件的顺序不定，但是取出的时候是按照时间顺序的
        3. procs_map是一个字典，procs创建一个它的副本，为了不改变proc_map。把出租车的编号映射到仿真过程中激活的进程（也就是出租车的生成器对象）
        """
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)
        """如果按照下面创立的taxi，那么procs_map和procs都应该为
        taxis = {
            0: taxi_process(ident=0, trips=2, start_time=0),
            1: taxi_process(ident=1, trips=4, start_time=5),
            2: taxi_process(ident=2, trips=6, start_time=10),
        }
        """

    def run(self, end_time):
        """排定并显示时间，直到时间结束"""
        #proc 表示各辆出租车的进程
        for _, proc in sorted(self.procs.items()): #用sorted函数获取self.procs中按值排序的元素。

            first_event = next(proc)  #在各辆出租车上调用next()，预激协程，向前执行到第一个yield表达式。
            # 这样会产出个辆出租车的第一个Event。
            self.events.put(first_event) #把各个事件放入Simulator类的self.events也就是队列中。


        sim_time = 0 #仿真钟归零
        while sim_time < end_time:  #如果sim_time < end_time，运行仿真系统的主循环
            if self.events.empty():  # 如果队列为空，跳出循环
                print('*** end of events ***')
                break

            current_event = self.events.get()  # 如果不为空，获取时间值最小的事件。因为PriorityQueue是按照时间排列的。
            sim_time, proc_id, previous_action = current_event  #获取event的各个属性，特别注意sim_time更新了
            print('taxi:', proc_id, proc_id * '   ', current_event)  #显示获取的Event
            active_proc = self.procs[proc_id] #从self.procs字典中获取表示当前活动的出租车的协程
            next_time = sim_time + compute_duration(previous_action)  # 更新仿真时间，compute_duration计算前一个动作花的时间
            try:
                next_event = active_proc.send(next_time)  # 把时间发给current_event的proc属性标识的协程，产生下一个事件或者抛出异常
            except StopIteration:
                del self.procs[proc_id]   #如果抛出异常，从self.procs字典中删除那个协程
            else:
                self.events.put(next_event)  #不然，把next_event放入队列中
        else:  #如果sim_time >= end_time，显示待完成的事件数量
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))
# END TAXI_SIMULATOR

def compute_duration(previous_action):
    """Compute action duration using exponential distribution"""
    """
    DEFAULT_NUMBER_OF_TAXIS = 3
    DEFAULT_END_TIME = 180
    SEARCH_DURATION = 5  
    TRIP_DURATION = 20
    DEPARTURE_INTERVAL = 5
    """

    if previous_action in ['leave garage', 'drop off passenger']:
        # new state is prowling
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # new state is trip
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    return int(random.expovariate(1/interval)) + 1 #Generate pseudo-random numbers

def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
         seed=None):
    """Initialize random generator, build procs and run simulation"""
    if seed is not None:
        random.seed(seed)  # get reproducible results

    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL) #taxi字典的值是三个参数不同的生成器对象。
             for i in range(num_taxis)} #例如下面：2号出租车从start_time = 10时开始，寻找6个乘客。

    sim = Simulator(taxis)  #实例化Simulator类
    """
    DEPARTURE_INTERVAL = 5
    num_taxis = 3
    那么上面的taxis可以写成
    taxis = {
    0: taxi_process(ident = 0, trips = 2, start_time = 0), 
    1: taxi_process(ident = 1, trips = 4, start_time = 5), 
    2: taxi_process(ident = 2, trips = 6, start_time = 10),
    }
    
    
    
    """
    sim.run(end_time) #各个出租车协程由run方法中的主循环驱动

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        description='Taxi fleet simulator.')
    parser.add_argument('-e', '--end-time', type=int,
                        default=DEFAULT_END_TIME,
                        help='simulation end time; default = %s'
                        % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int,
                        default=DEFAULT_NUMBER_OF_TAXIS,
                        help='number of taxis running; default = %s'
                        % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='random generator seed (for testing)')

    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)


"""
输出：
taxi: 0  Event(time=0, proc=0, action='leave garage')
taxi: 0  Event(time=1, proc=0, action='pick up passenger')
taxi: 1     Event(time=5, proc=1, action='leave garage')
taxi: 1     Event(time=6, proc=1, action='pick up passenger')
taxi: 2        Event(time=10, proc=2, action='leave garage')
taxi: 2        Event(time=15, proc=2, action='pick up passenger')
taxi: 0  Event(time=17, proc=0, action='drop off passenger')
taxi: 0  Event(time=22, proc=0, action='pick up passenger')
taxi: 0  Event(time=27, proc=0, action='drop off passenger')
taxi: 0  Event(time=28, proc=0, action='going home')
taxi: 1     Event(time=28, proc=1, action='drop off passenger')
taxi: 1     Event(time=36, proc=1, action='pick up passenger')
taxi: 1     Event(time=38, proc=1, action='drop off passenger')
taxi: 1     Event(time=41, proc=1, action='pick up passenger')
taxi: 1     Event(time=45, proc=1, action='drop off passenger')
taxi: 1     Event(time=47, proc=1, action='pick up passenger')
taxi: 1     Event(time=79, proc=1, action='drop off passenger')
taxi: 1     Event(time=82, proc=1, action='going home')
taxi: 2        Event(time=91, proc=2, action='drop off passenger')
taxi: 2        Event(time=95, proc=2, action='pick up passenger')
taxi: 2        Event(time=97, proc=2, action='drop off passenger')
taxi: 2        Event(time=101, proc=2, action='pick up passenger')
taxi: 2        Event(time=138, proc=2, action='drop off passenger')
taxi: 2        Event(time=146, proc=2, action='pick up passenger')
taxi: 2        Event(time=151, proc=2, action='drop off passenger')
taxi: 2        Event(time=152, proc=2, action='pick up passenger')
taxi: 2        Event(time=153, proc=2, action='drop off passenger')
taxi: 2        Event(time=157, proc=2, action='pick up passenger')
taxi: 2        Event(time=187, proc=2, action='drop off passenger')
*** end of simulation time: 1 events pending ***
"""

```
































