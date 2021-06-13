
#概念
#1. 继承：子类拥有父类的所有方法和属性，相同的代码不需要重复的编写

#2. 重写：当父类的方法实现不能满足子类需求时，可以对方法进行重写
#有两种方式可以进行重写：
#2.1 覆盖父类的方法
#在子类中定义一个和父类同名的方法并且实现
#重写之后，在运行时，只会调用子类重写之后的方法，不会调用父类的方法

#2.2 对父类方法进行拓展（父类中的方法是子类方法的一部分）
# 在子类中使用super().父类方法来调用父类方法
# 针对子类的需求，编写子类自己的代码



#3. 父类的私有属性和私有方法
#3.1 子类对象不能在自己的方法内部，直接访问父类的私有属性或私有方法
#3.2 子类对象可以通过父类的公有方法，间接访问到私有属性或私有方法



#4.多继承
#子类可以继承多个父类
#子类会按照mro方法搜索继承的顺序
#MRO 就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表。
# 按照__mro__的输出结果从左至右搜索，如果在当前类中找到方法，就直接执行，不再搜索。如果没有找到，就查找下一个类




#4.3 怎么理解super
"""
super() 函数是用于调用父类(超类)的一个方法。
super(class, obj),它返回的是obj的MRO中class类的父类
super() 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题

"""

#5.新式类与旧式类
#新式类：以 object 为基类的类，推荐使用
#经典类：不以 object 为基类的类，不推荐使用











