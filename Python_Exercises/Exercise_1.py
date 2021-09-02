
#href: https://zhuanlan.zhihu.com/p/393058336 Python编程与Office办公自动化

#1.将列表转化为字典
keys = ['one','two','three']
values = [1,2,3]

dic = dict(zip(keys,values))  # {'one': 1, 'two': 2, 'three': 3}


#2.将下面的两个Python词典合并
#注：字典可用**拆解，拆解出来就是字典的每一项
dic1 = {'one': 1, 'two': 2, 'three': 3}
dic2 = {'three': 3, 'four': 4, 'five': 5}
dic3 = {**dic1,**dic2}   #{'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}

#3.获取字典中的值：获取下列字典键为'history'的值
sampleDict = {
   "class":{
      "student":{
         "name":"Mike",
         "marks":{
            "physics":70,
            "history":80
         }
      }
   }
}

sampleDict["class"]["student"]["marks"]["history"]  #80


#4：将下面字典中部分件提取出来成为新的字典

sampleDict = {
    "name": "Kelly",
    "age": 25,
    "salary": 8000,
    "city": "New york"

}

keys = ["name", "salary"]

newDict = {key:sampleDict[key] for key in keys} #{'name': 'Kelly', 'salary': 8000}


#5. 从字典中删除一组键
sampleDict = {
    "name": "Kelly",
    "age": 25,
    "salary": 8000,
    "city": "New york"

}
keysToRemove = ["name", "salary"]

newDict = {key:sampleDict[key] for key in sampleDict.keys()- keysToRemove } #{'age': 25, 'city': 'New york'}

#6.反转给定列表中的各元素
aLsit = [100, 200, 300, 400, 500]
aLsit[::-1]  #[500、400、300、200、100]


#7.按索引连接两个列表
list1 = ["M", "na", "i", "Ke"]
list2 = ["y", "me", "s", "lly"]
l = [i + j for i,j in zip(list1,list2)]  #['My', 'name', 'is', 'Kelly']


#8.给定一个数字列表，将列表中的每一项的平方数
aList = [1, 2, 3, 4, 5, 6, 7]
l = [a**2 for a in aList] #[1, 4, 9, 16, 25, 36, 49]
print(l)

#9.依次按顺序连接两个列表
list1 = ["Hello ", "take "]
list2 = ["Dear", "Sir"]
#['Hello Dear', 'Hello Sir', 'take Dear', 'take Sir']

l = [a+b for a in list1 for b in list2]

#10.同时迭代两个列表，以便 list1 应按原始顺序显示元素，而 list2 应按相反顺序显示元素
list1 = [10, 20, 30, 40]
list2 = [100, 200, 300, 400]

for x,y in zip(list1,list2[::-1]):
    print(x,y)


#11.给定一个字符串和一个整数 n，从字符串中删除从 0 到 n 的字符并返回一个新字符串
#例如，removeChars("人生苦短，我爱Python", 5)因此输出必须为我爱Python.注意：n必须小于字符串的长度
def removeChars(s,n):
    return s[n:]


print(removeChars("人生苦短，我爱Python", 5))  #我爱Python

#12.输出偶数索引号处的字符
#给定一个字符串，只显示出现在偶数索引号处的那些字符 例如:str = "Python"您应该显示p、t、o
s = 'hellopython'
for i in range(0,len(s),2):
    print(s[i])

