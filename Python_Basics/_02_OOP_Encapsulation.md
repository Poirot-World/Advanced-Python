

#第一部分：概念

#1. 什么是面向对象编程？好处
#面向过程：把解决问题的方法一步一步用函数实现，再按顺序调用不同的函数。
# 注意：数据和函数时分开的（解决该怎么做：自己一步一步做）
#面向对象：根据职责确定不同的对象，在对象内部封装不同的方法。再让不同的对象调用不同的方法解决问题
# 注意：因为对象可以存储数据，所以数据和函数结合在一起（解决谁来做：交给对象来做）

#2.类和对象
#对象：
#对象是现实世界的具体东西。对象具备特征或行为。

#类
#先有对象后有类。类是最一群具有相同特征或者行为事物的抽象。
#特征被称为属性
#行为被称为方法

#编码上，先有类再有对象（实例化）
#设计上，先有对象再有类（抽象）

#3. 怎么设计一个类
#类名是大驼峰命名法（每一个单词首字母大写；单词紧挨着）+确定属性+确定方法

#第二部分：类

#1. 内置函数
#dir() 可以查看对象内所有的属性以及方法
#__new__：创建对象时，会被自动调用
#__init__：对象被初始化时，会被自动调用
#__del__：对象被从内存中销毁前，会被自动调用
#__str__：返回对象的描述信息

#2. 通过一个例子来看一下类的基本使用
#例子1：



# class Cat:
#     """这是一个猫类"""
#
#     # 生命周期：一个对象被创建到被销毁的过程。
#     # 创建一个对象：开辟一块内存，调用__init__方法，生命周期开始。
#     # 销毁一个对象：调用 __del__ 方法，生命周期结束。
#     def __init__(self,name):
#         self.name = name
#     def __del__(self):
#         pass
#
#     def __str__(self):
#         return "我是小猫：%s" %self.name
#
#     def eat(self):
#         print("%s 爱吃鱼" %self.name)
#
#     def drink(self):
#         print("%s 在喝水" %self.name)
# #tom和tim记录的是对象在内存中的地址
# # 用引用来理解就是，先创建对象（也就是创建一块内存空间），然后tom这个变量贴到0x104a2cb80这块内存空间上。
# tom = Cat("tom")
# tim = Cat("tim")
# #用print打印变量tim和tom。
# print(tom)
# print(tim)
"""
__str__方法与print方法的不同
#开发中使用__str__方法，用户使用print方法。
1. 类没有定义 def __str__(self)这个函数时，执行print(tom) print(tim)。
会输出这两个变量引用的对象是由哪一个类创建的对象，并且会打印出内存中的地址。
--> <__main__.Cat object at 0x104a2cb80>
--> <__main__.Cat object at 0x104a2cf70>
2. 类定义了__str__时，用print(tom)打印对象变量，能够打印自定义的内容。
我是小猫：tom
我是小猫：tim

"""


# tim.drink()  #哪一个对象调用的方法，方法内的self就是哪一个对象的引用
#-->tim 在喝水

#3.通过一个例子来看一下类的私有属性和私有方法
#私有属性和私有方法：对象不希望被外部访问的属性的方法
#如何做：定义的时候，在属性名或者方法名前增加双下线
#用_类名__名称访问私有属性
#例子2：

class Women:
    def __init__(self,name):
        self.name = name
        self.__age = 20

    def __secret(self):
        print("我的年龄是%d" %self.__age)

Strom = Women("Strom")
# print(Strom.__age)
#print(Strom.__secret())
# 不能访问
#但是Python中没有绝对意义的私有，用_类名__名称还是可以访问到
print("Strom的年龄是%d" %Strom._Women__age)
#->Strom的年龄是20
Strom._Women__secret()
#->我的年龄是20

# 4.通过一个例子来看一下类的封装
#封装：将属性和方法封装到一个类中
#如何使用：用类创建一个对象，然后让对象调用方法。
#例子3：
"""
需求：
1. 士兵许三多有一把AK47
2. 士兵可以开火
3. 枪能够发射子弹
4. 枪装填子弹
"""

class Soldier():

    def __init__(self,name,gun =None):
        self.name = name
        self.gun = gun

    def fire(self):
        #判断士兵是否有枪
        if self.gun is None:
            print("%s还没有枪" %self.name)
            return
        print("装填子弹")
        self.gun.add_bullet(10)   #让自己的属性调用其他类的方法
        print("开火")
        self.gun.shoot()

class Gun():
    def __init__(self, model):
        self.model = model
        self.bullet_count = 0

    def shoot(self):
        #判断是否还有子弹
        if self.bullet_count <= 0:
            print("没有子弹了")
            return
        print("%s发射子弹" %(self.model))
        self.bullet_count -= 1
        print("还剩%d颗子弹"%(self.bullet_count))

    def add_bullet(self,count):
        print("装%d颗子弹" %(count))
        self.bullet_count += count
        print("目前有%d颗子弹" %(self.bullet_count))

gun = Gun("AK47")
xusanduo = Soldier("许三多",gun)

xusanduo.fire()
xusanduo.gun.add_bullet(10)


"""
装填子弹
装10颗子弹
目前有10颗子弹
开火
AK47发射子弹
还剩9颗子弹
装10颗子弹
目前有19颗子弹
"""





