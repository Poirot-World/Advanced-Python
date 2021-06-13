#概念
#多态：不同的子类调用相同的父类方法，产生不同的结果
#以继承和重写父类方法为前提

class Animal(object):   #编写Animal类
    def run(self):
        print("Animal is running...")

class Dog(Animal):  #Dog类继承Amimal类，没有run方法
    pass

class Cat(Animal):  #Cat类继承Animal类，有自己的run方法
    def run(self):
        print('Cat is running...')
    pass

class Car(object):  #Car类不继承，有自己的run方法
    def run(self):
        print('Car is running...')

class Stone(object):  #Stone类不继承，也没有run方法
    pass

def run_twice(animal):
    animal.run()
    animal.run()

run_twice(Animal())
run_twice(Dog())
run_twice(Cat())
run_twice(Car())
run_twice(Stone())

#对于一个变量，我们只需要知道它是Animal类型，无需确切地知道它的子类型，就可以放心地调用run()方法
# 而具体调用的run()方法是作用在Animal、Dog、Cat还是Tortoise对象上，由运行时该对象的确切类型决定
# 这就是多态真正的威力：调用方只管调用，不管细节，而当我们新增一种Animal的子类时
# 只要确保run()方法编写正确，不用管原来的代码是如何调用的。



#继承与多态的区别：
#继承允许已存在的代码在程序中再次重用，而多态性提供了一种机制，可以动态地决定要调用的函数形式。
