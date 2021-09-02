"""
#可散列的数据类型定义：如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的.
# 而且这个对象需要实现__hash__()方法和__eq__()方法。
#例子：原子不可变数据类型（str,bytes和数值类型）和frozenset是可散列类型。
#元组不一定:只有当元组中包含的所有元素都是可散列类型的情况下才是可散列的
tt = (1,2,(3,4))
print(hash(tt))  #3794340727080330424
t = (1,2,[3,4])
print(hash(t))  #unhashable type: 'list'



#如果一个对象实现了__eq__方法，并且在方法中用到了这个对象的内部状态的话，
# 那么只有当所有这些内部状态都是不可变的情况下，这个对象才是可散列的。
class A:
    def __init__(self, a_):
        self.a = a_

    def __hash__(self):
        return hash(self.a)

    def __eq__(self, other):
        return hash(self) == hash(other)


a1 = A(1)
a2 = A([1,2])
a3 = A((1,2))
print(hash(a1)) # -->1
print(hash(a2)) # unhashable type: 'list'
print(hash(a3))  #-3550055125485641917

"""
#字典构造方法
a = dict(one = 1, two = 2, three = 3)
b = {'one':1,'two':2,'three':3}
c = dict(zip(['one','two','three'],[1,2,3]))
d = dict([('two',2),('one',1),('three',3)])
e = dict({'three':3,'one':1,'two':2})
print(a==b==c==d==e)  #True

#字典推导式：可以从任何以键值对作为元素的可迭代对象中构建出字典

l = [('two',2),('one',1),('three',3)] #l是有成对数据的列表
d = {word:number for word,number in l if number >2}
print(d)


#常见的映射方法dict,collections.defaultdict和collections.OrderedDict




#如果处理查找不到的键
#标准库中dict类型的变种
#set和frozenset类型

s = set(1)
print(s)
print(hash(s))
