#1.标识，值，别名
#注意：变量是标注，不是盒子
#创建对象时，对象就有了唯一标识，也就是对象在内存中的地址。id()可以返回对象的标识
#"=="和"is"的不同："=="比较值，"is"比较标识。用不着用id()判断标识是否一样。
#别名和原始数据块具有同一标识。

#2.赋值，深拷贝和浅拷贝的不同
#不可变对象：字符串，元组，数值类型，复制不可变对象不会开辟新的内存空间
#可变对象：列表，字典，集合


"""
#赋值：不会开辟新的内存空间，只是在原始数据块上贴个标签。原始数据块和副本互相影响。
l = (1,2,3,[4,5]) #外层不可变对象
l1 = l
l1[3].append(6)
l[3].append(7)
print(l,l1)  #(1, 2, 3, [4, 5, 6, 7]) (1, 2, 3, [4, 5, 6, 7])
print(l is l1)  #True

t = [1,2,3]  #外层可变对象
t1 = t
t1.append(4)
t.append(5)
print(t,t1)  #[1, 2, 3, 4, 5] [1, 2, 3, 4, 5]
print(t is t1)  #True


#浅拷贝（切片操作，工厂函数，copy函数）
#浅拷贝有三种可能性：

#当浅拷贝的原始数据块（外层）是不可变对象，无论内层是什么对象，不会开辟内存空间。
l_shallow = (1,2,3,[4,5])  #外层不可变对象
l_shallow_1 = tuple(l_shallow)
l_shallow_1[3].append(6)
l_shallow[3].append(7)
print(l_shallow,l_shallow_1) #(1, 2, 3, [4, 5, 6, 7]) (1, 2, 3, [4, 5, 6, 7])
print(l_shallow is l_shallow_1)  #True

#当浅拷贝的原始数据块（外层）是可变对象。
#当数据块的元素（内层）是不可变对象，会开辟内存空间。外层改变原始数据块和副本不会互相影响。
t_shallow = [1,2,3,(4,5)]  #外层可变对象，内层不可变对象
t_shallow_1 = t_shallow[:]
t_shallow.append(6)  #外层添加6
t_shallow_1.append(7)  #外层添加7
print(t_shallow,t_shallow_1)  #[1, 2, 3, (4, 5), 6] [1, 2, 3, (4, 5), 7]
print(t_shallow is t_shallow_1)  # False

#当浅拷贝的原始数据块（外层）是可变对象。
#当数据块的元素（内层）是可变对象，会开辟内存空间。外层改变互不影响，内层改变互相影响。
import copy
s_shallow =  [1,2,3,[4,5]]  #外层可变对象，内层可变对象
s_shallow_1 = copy.copy(s_shallow)
print(s_shallow is s_shallow_1)  #False
s_shallow.append(6)
s_shallow_1.append(7)
s_shallow[3].append(8)
s_shallow_1[3].append(9)
print(s_shallow,s_shallow_1)  #[1, 2, 3, [4, 5, 8, 9], 6] [1, 2, 3, [4, 5, 8, 9], 7]



#深拷贝：会开辟空间，互不影响。
import copy
#外层不可变，会开辟内存空间，原始数据块和副本互不影响
l_deep = (1,2,3,[4,5])
l_deep_1 = copy.deepcopy(l_deep)
print(l_deep_1 is l_deep) #False
l_deep[3].append(6)
l_deep_1[3].append(7)
print(l_deep,l_deep_1)  #(1, 2, 3, [4, 5, 6, 7]) (1, 2, 3, [4, 5, 6, 7])


#外层可变，开辟新的内存空间。外层改变互不影响，内层改变互不影响。
t_deep = [1,2,3,(4,5),[6,7]]
t_deep_1 = copy.deepcopy(t_deep)
print(t_deep_1 is t_deep)  #False
t_deep.append(8)  #外层改变
t_deep_1.append(9) #外层改变
t_deep[4].append(8)  #内层改变
t_deep_1[4].append(9) ##内层改变

print(t_deep,t_deep_1)  #[1, 2, 3, (4, 5), [6, 7, 8], 8] [1, 2, 3, (4, 5), [6, 7, 9], 9]



#3.引用和函数参数：可变的参数默认值导致的问题，以及如何安全地处理函数的调用者传入的可变参数。
#共享传参：函数的形参是实参的引用的副本。
#函数内部可能会修改传入的可变对象。例子1：
def f(a,b):
    a += b
    return a
a, b = [1,2],[3,4]
f(a,b)
print(a,b)  #[1, 2, 3, 4] [3, 4]


#避免使用可变的对象作为参数的默认值。例子2：
#如果默认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影响。就像下面的bus2和bus3
class HauntedBus:
    def __init__(self, passengers=[]): #如果没有传入passengers参数，一开始的默认值是空列表。
        self.passengers = passengers  #赋值操作，赋值就是别名
    def pick(self, name):
        self.passengers.append(name)
    def drop(self,name):
        self.passengers.remove(name)


bus2 = HauntedBus()
bus2.pick('CC')
print(bus2.passengers)  #['CC']
bus3 = HauntedBus() #bus3用的默认列表，但是默认列表不为空
print(bus3.passengers)  #['CC']
bus3.pick('D')
print(bus2.passengers) #['CC', 'D']
print(bus2.passengers is bus3.passengers) #True

#防御可变参数
#例子3解决例子2的问题：用None作为接收可变值的参数的默认值
#例子3出现新的问题：在self.passengers调用.remove()和.append()，会修改__init__方法里面的passengers

class TwilightBus:
    def __init__(self, passengers = None): #passengers是__init__方法的实参
        if passengers is None:  #解决上面的问题
            self.passengers = []
        else:
            self.passengers = passengers #把self.passengers变成passengers的别名
    def pick(self,name):
        self.passengers.append(name) #在self.passengers调用.remove()，会修改__init__方法里面的passengers
    def drop(self,name):
        return self.passengers.remove(name)


basketball_team = ['Sue','Tina','Maya','Diana','Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)  #['Sue', 'Maya', 'Diana']


#例子4解决例子3的问题：不为None的时候用浅拷贝，而不是直接赋值
#把passengers的副本赋值给self.passengers，这样basketball_team不会由于类内部的操作而改变
#前面总结的：浅拷贝，外层是可变对象，外层改变，原始数据和副本互不影响。

class TwilightBus:
    def __init__(self, passengers = None): #passengers是__init__方法的实参
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers) #把passengers的副本赋值给self.passengers
    def pick(self,name):
        self.passengers.append(name) #在self.passengers调用.remove()，不会修改__init__方法里面的passengers
    def drop(self,name):
        return self.passengers.remove(name)

basketball_team = ['Sue','Tina','Maya','Diana','Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)  #['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
"""
#4.垃圾回收、del命令
#没有对象的引用了，对象就结束了。
#垃圾回收的算法是引用计数：每个对象都会统计有多少引用指向自己，当引用计数归零，对象立即被销毁。
#注意：del语句删除名称，不是对象。也就是说，删除标注，不是删除内存空间。
#例子5
import weakref
s1 = {1, 2, 3}
s2 = s1 #s2是s1的别名
def bye():
    print('Gone with the wind...')

ender = weakref.finalize(s1,bye) #在s1引用的对象上注册bye回调
print(ender.alive)  #True
del s1        #del不删除对象，而是删除对象的引用s1
print(ender.alive)  #True
s2 = 'spam'  #Gone with the wind...  #重新绑定最后一个引用，对象{1,2,3}没有引用了，所以被销毁了，调用bye
print(ender.alive)  #False

# 弱引用