### 背景：生成器中的yield和协程中的yield的作用不一样

- 生成器中yield有两个作用： 

1. 会产出一个值，提供给next()调用方
2. 让步，暂停执行生成器，让调用方继续工作


- 协程中，yield是一种控制流程的方式，它把控制器让步给中心调度程序。
1. 协程中，yield出现在表达式的右边。
2. yield主要的作用是：</br>
   a. yield用于暂停执行携程，把产出发给调用方</br>
   b. yield接受调用方发给协程的值

### 第一部分：生成器作为协程使用时的行为和状态

#### 例子一：产出一个值的协程

生成器的调用方可以使用.send(...)方法发送数据，发送的数据会成为生成器函数中yield表达式的值。

```python

def simple_coroutine():
    print('-> coroutine1 started')
    '''
    解释：
    1. 协程中yield在表达式右侧
    2.如果yield右侧没有其他表达式，产出值为None
    3. 协程在yiled关键字所在的位置暂停执行。
    
    '''
    x = yield
    print('-> coroutine1 received:', x)

my_coro = simple_coroutine() 
#my_coro是生成器对象



next(my_coro)
'''
输出：-> coroutine1 started
解释：
1. 如果没有先调用.next()会出现错误
can't send non-None value to a just-started generator
2. yiled的表达式接收42，程序运行，运行后面的print语句。
程序会一直运行到下一个yield表达式
3. next(my_coro)叫做预激协程。
意思就是让协程执行到第一个yiled表达式，准备好作为活跃的协程使用
'''

my_coro.send(42)   
#输出：-> coroutine1 received: 42


```

#### 例子二：产出两个值的协程
协程在yield关键字所在的位置暂停执行。</br>
先执行右边的等式，然后停下来，等待。
```python
def simple_coro2(a):
    
    print('-> Start: a =', a)
    b = yield a
    print('-> Received: b = ',b)
    c = yield a + b
    print('-> Received: c =', c)

my_coro2 = simple_coro2(14)

next(my_coro2)
'''
输出：
-> coroutine started
-> Start: a = 14
解释：预激协程，执行到第一个yield表达式的右边 a，然后等待。
注意此时产出的值是14，如果执行a = next(my_coro2)和print(a)，
那么可以看到14被打印出来。
'''

my_coro2.send(28)
'''
输出：
-> Received: b =  28
解释：调用方把28发给协程，
此时b = yield，执行到下一个yield表达式的右边 a + b，
然后等待（注意此时产出的值是42）
'''

my_coro2.send(99)
'''
输出：
-> Received: c = 99
解释：调用方把99发给协程，此时 c =yield ，协程终止（此时产出的值是99）
'''
```

#### 例子三：协程的四个状态。
可以用inspect.getgeneratorstate(...)查询
- 'GEN_CREATED'
- 'GEN_RUNNING'
- 'GEN_SUSPENDED'
- 'GEN_CLOSED'

```python
from inspect import getgeneratorstate
def simple_coro3():
    x = yield
    print(x)


my_coro3 = simple_coro3()
print(getgeneratorstate(my_coro3))
'''
输出：
'GEN_CREATED'
 解释：协程未启动
'''

next(my_coro3)
print(getgeneratorstate(my_coro3))
'''
输出：
'GEN_SUSPENDED' 
 解释：协程在yield表达式处暂停
'''

my_coro3.send(29)
print(getgeneratorstate(my_coro3))
'''
输出：
'GEN_CLOSED'
 解释：协程执行结束
'''
```

#### 例子四 使用闭包和协程计算移动平均值
协程只需声明局部变量，闭包要声明自由变量。

##### 使用闭包

```python
def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total #把变量标记为自由变量
        count += 1
        total += new_value
        return total/count
    return averager    #返回一个averager对象

a = make_averager()

print(a(10))
'''
输出：
10.0
'''

print(a(5))
'''
输出：
7.5
'''
```

##### 使用协程

yield右边的表达式产生值（返回给调用方），左边的表达式接收值。
```python
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count
        
coro_avg = averager()
next(coro_avg)
a = coro_avg.send(10)
print(a)  # 10.0
b = coro_avg.send(20)
print(b)  # 15.0
```

### 第二部分：使用装饰器自动预激协程

#### 例子一:写一个装饰器，功能是primer coroutine
```python
from functools import wraps
def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

```





[comment]: <> (#调用方如何使用生成器对象的.close&#40;&#41;和.throw&#40;&#41;方法控制协程)

[comment]: <> (#hou者的作用是让调用方抛出异常，在生成器中处理；qian者的作用是终止生成器)

[comment]: <> (#协程终止时如何返回值)

[comment]: <> (#yield from 新句法的用途和语义)

[comment]: <> (#使用协程管理仿真系统中的并发活动)











