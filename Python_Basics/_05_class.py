#类属性和类方法

#除了实例属性和实例方法之外，还有类属性和类方法

#1. 类属性就是在类中定义的属性，通常记录与这个类相关的特征，不会记录单个实例的特征


class Tool(object):

    # 使用赋值语句，定义类属性，记录创建工具对象的总数
    count = 0

    def __init__(self, name):
        self.name = name

        # 针对类属性做一个计数+1
        Tool.count += 1


# 创建工具对象
tool1 = Tool("斧头")
#查找属性存在一个向上查找机制：首先在实例属性查找，找不到就去类属性查找
tool2 = Tool("榔头")
tool3 = Tool("铁锹")

# 知道使用 Tool 类到底创建了多少个对象?
print("现在创建了 %d 个工具" % Tool.count)
#-># 工具对象的总数 1

#2. 类方法
#类方法就是针对类对象定义的方法，可以通过cls访问类属性或者其他类方法
#类方法需要装饰器@classmethod来告诉解释器这是一个类方法
#类方法的第一个参数是cls
"""
@classmethod
def 类方法名(cls):
    pass
"""
class Tool(object):

    # 使用赋值语句，定义类属性，记录创建工具对象的总数
    count = 0

    @classmethod
    def show_tool_count(cls):
        """显示工具对象的总数"""
        print("工具对象的总数 %d" % cls.count)

    def __init__(self, name):
        self.name = name

        # 针对类属性做一个计数+1
        Tool.count += 1

Tool.show_tool_count()  # 工具对象的总数 0
tool = Tool("铁锹")
Tool.show_tool_count()  # 工具对象的总数 1

#3. 静态方法
#既不需要访问实例属性和实例方法，也不需要访问类属性和类方法
"""
@staticmethod
def 静态方法名():
    pass
"""
#静态方法需要修饰器@staticmethod来告诉解释器这是一个静态方法

class Dog(object):
    # 狗对象计数
    dog_count = 0

    @staticmethod
    def run():
        # 不需要访问实例属性也不需要访问类属性的方法
        print("狗在跑...")

    def __init__(self, name):
        self.name = name

Dog.run()
#->狗在跑...


#例子：
"""
需求：
设计一个Game类
1.查看帮助信息
2.查看历史最高分
3.创建游戏对象，开始游戏
"""

class Game(object):
    #类属性
    top_score = 100

    #类方法
    @classmethod
    def show_top_score(cls):
        print("历史最高分是%d" % cls.top_score)

    # 实例属性
    def __init__(self,name):
        self.player_name = name

    # 实例方法
    def start_game(self):
        print("%s开始玩游戏！" %self.player_name)

        #修改类属性
        Game.top_score = 110

    #静态方法
    @staticmethod
    def show_help():
        print("游戏帮助信息")

#查看帮助信息
Game.show_help()
#->游戏帮助信息

#查看历史最高分
Game.show_top_score()
#->历史最高分是100

#创建游戏对象，开始游戏
xiaowang = Game("xiaowang")
xiaowang.start_game()
#->xiaowang开始玩游戏！

Game.show_top_score()
#->历史最高分是110