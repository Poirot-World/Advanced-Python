### 第一部分：with语句和上下文管理器

`with open('mirror.py') as fp`

1. with open('mirror.py') as fp叫上下文表达式。
2. 执行了open('mirror.py')，就获得了上下文管理器，也叫上下文管理器对象。
3. 上下文管理器对象是实现了__enter__和__exit__两个方法的对象。
4. with语句开始运行时，会在上下文管理器对象上调用__enter__方法。
5. with语句运行结束后，会在上下文管理器对象上调用__exit__方法。
6. with的作用是确保代码运行完以后执行某项操作，释放重要的资源，还原变更的状态
7. as后面保存的是__enter__方法的返回值，如果返回None则不用加as

#### 例子1：构造一个LookingGlass上下文管理器类
```python
class LookingGlass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write #把原来的sys.stdout.write方法保存在一个实例属性中，供后面使用
        sys.stdout.write = self.reverse_write #为sys.stdout.write打猴子补丁，替换成自己编写的方法。
        return 'Bestes Leben' #返回'Bestes Leben'字符串，这样才有内容存入目标变量what。
    def reverse_write(self,text):
        self.original_write(text[::-1]) #取代sys.stdout.write的方法，实现内容反转
    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stdout.write = self.original_write #还原成原来的sys.stdout.write方法。
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True


```

#### 例子2：测试上面的上下文管理器类
```python

with LookingGlass() as what: #Python在上下文管理器上调用__enter__方法，把返回结果绑定到what上。

    print('Alice, Kitty and Snowdrop')
    print(what)
#-->pordwonS dna yttiK ,ecilA
#-->nebeL setseB  #with执行完毕之前，在LookingGlass这个类中，但凡有输出，都要倒序输出
print(what)
#-->Bestes Leben

```

### 第二部分：contextlib和@contextmanager装饰器

1. @contextmanager装饰器使用yield语句
2. yield语句前面的所有代码在with块开始时（即解释器调用__enter__方法时）执行
3. yield语句后面的代码在with块结束时（即调用__exit__方法时）执行。

#### 例子3：用yield实现with的作用
```python
import contextlib
@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write
    def reverse_write(text):
        original_write(text[::-1])
    sys.stdout.write = reverse_write
    yield 'Bestes Leben'
    sys.stdout.write = original_write

```

#### 例子4：测试looking_glass类
```python
with looking_glass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)
#-->pordwonS dna yttiK ,ecilA
#-->nebeL setseB
print(what)
#-->Bestes Leben
```

####例子5：给例子3加上异常管理：必须要用try finally
```python
import contextlib
@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write
    def reverse_write(text):
        original_write(text[::-1])
    sys.stdout.write = reverse_write
    msg = '' #msg用于保存可能出现的错误信息
    try:
        yield 'Bestes Leben'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)

```

###第三部分：for,while和try语句的else子句
注意：else与for, while 或者try搭配使用相当于then。</br>
####例子1： 在循环中使用else：运行这个循环之后，运行else里面的语句。
```python
for item in items:
    if item.flavor == 'banana':
        break
else:
    raise ValueError('No banana flavor found!')

```
####例子2：仅当try块中没有异常抛出时才运行else块。
```python
#try官方文档还指出：“else子句抛出的异常不会由前面的except子句处理。”

try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()
```

####例子3：先执行while中间的语句，当while条件不满足时，执行else中间的语句
```python
count = 0
while count < 2:
   print (count, " is  less than 2")
   count = count + 1
else:
   print (count, " is not less than 2")
   
#-->0  is  less than 2
#-->1  is  less than 2
#--> 2  is not less than 2

```


