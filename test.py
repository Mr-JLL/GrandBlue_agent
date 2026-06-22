import requests

# 返回较大数 
def returnum(a,b):
    return max(a,b)
print(returnum(1,2))


# 写一个函数，接收一个列表，返回其中所有偶数 
# numlist=[] 
# numlist=[] 必须写在函数里面，如果写在函数外面的话那么它从程序启动就一直存在，从来不清空，每次调用函数都是往同一个列表里添加，上次的结果不会消失  
def get_evens(lst):
    numlist=[]
    for item in lst:
        if item%2==0:
            numlist.append(item)
    return numlist
#   为什么print()不放在return后面，因为执行完return后会立刻退出函数，后面的任何代码都不会运行 
#   print(get_evens(lst))
print(get_evens([1,2,3,4]))



# 写一个类，代表一个学生，有姓名和成绩，有一个方法返回是否及格
class Student():
    def __init__(self,name,grade):
        self.name=name
        self.grade=grade

    def NailedOrNot(self):
        if self.grade < 60:
            print("不合格")
        else:
            print("合格！")
XiaoMing=Student('XiaoMing',60)
XiaoMing.NailedOrNot()


# 写一个函数，读取一个文本文件，返回行数 


# 写一个函数，用 requests 库访问 https://httpbin.org/get，打印返回的 JSON
response=requests.get("https://httpbin.org/get")
data=response.json()

print(data)


