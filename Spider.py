'''
本模块的任务是获取求职内容信息，包括职位名称，地点，薪资和岗位要求，并打印出
名称，地点，薪资和统计出现次数最多的工作要求
'''

import re #引入正则模块
from urllib import request #引入数据请求模块
from spider3 import Spider3 #获取求职列表信息（如第一页的所有列表等）
from spider4 import Spider4 #获取求职页面信息（如第一页，第二页等）
'''
以下代码的作用是将命令行内容输出
import sys
class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger("D:\\12.txt")
'''


#=================================================

class Spider():

    '''
    将Spider3的网址传输过来
    '''
    def __init__(self, url):
        self.url = url

    '''
    获取基本信息
    '''
    root_pattern = '<div class="tCompany_center clearfix">[\s\S]*?<div class="mt10">' #相关信息正则表达式-类变量
    name_pattern = '<h1 title="([\s\S]*?)">' #相关名字正则表达式-类变量
    address_pattern = '<p class="msg ltype" title="([\s\S]*?)&nbsp' #相关地址正则表达式-类变量
    salary_pattern = '<strong>([\s\S]*?)</strong>' #相关薪水正则表达式-类变量
    command_pattern = '<div class="bmsg job_msg inbox">([\s\S]*?)<div class="mt10">' #相关岗位要求正则表达式-类变量
    
    '''
    抓取数据方法fetch_content
    '''
    def fetch_content(self):
        r = request.urlopen(self.url) #调用request的urlopen方法
        htmls = r.read()
        htmls = str(htmls,encoding='gbk',errors='ignore')
        return htmls

    '''
    数据分析方法__analysis
    '''
    def analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            address = re.findall(Spider.address_pattern, html)
            salary = re.findall(Spider.salary_pattern, html)
            command = re.findall(Spider.command_pattern, html)
            # 以下代码的作用是去除无义字符
            command[0] = command[0].replace('<p>','')
            command[0] = command[0].replace('</p>','')
            command[0] = command[0].replace('&nbsp;','')
            command[0] = command[0].replace('<span>-','')
            command[0] = command[0].replace('<span>','')
            command[0] = command[0].replace('</span>-','')
            command[0] = command[0].replace('<div>','')
            command[0] = command[0].replace('</div>','')
            command[0] = command[0].replace('<b>','')
            command[0] = command[0].replace('</b>','')
            command[0] = command[0].replace('<i>','')
            command[0] = command[0].replace('</i>','')
            command[0] = command[0].replace('<u>','')
            command[0] = command[0].replace('</u>','')
            command[0] = command[0].replace('<li>','')
            command[0] = command[0].replace('</li>','')
            command[0] = str(command[0].replace(':',"\n"))
            command[0] = str(command[0].replace('：',"\n"))
            command[0] = str(command[0].replace(';',"\n"))
            command[0] = str(command[0].replace('；',"\n"))
            command[0] = str(command[0].replace('<br>',"\n"))
            command[0] = str(command[0].replace('<br/>',"\n"))
            command[0] = str(command[0].replace('<。>',"\n"))
            anchor = {'name':name,'address':address,'salary':salary,'command':command}
            anchors.append(anchor)
        return anchors

    '''
    数据精炼方法refine
    '''
    def refine(self, anchors):
        l =  lambda anchor: {
            'name':anchor['name'][0].strip(),
            'address':anchor['address'][0].strip(),
            'salary':anchor['salary'][0].strip(),
            'command':anchor['command'][0].strip()
            }
        return map(l, anchors)

    '''
    show方法，用于打印名称，地点和薪资，并分离出岗位要求
    '''
    def show(self, anchors):
        command_s = [] #用来接收岗位要求进行进一步分析
        for rank in range(0, len(anchors)):
            # 打印名称，地址和薪资
            print(anchors[rank]['name']
            + '   ' + anchors[rank]['address']
            + '   ' + anchors[rank]['salary'])
            command_s.append(anchors[rank]['command'])
        return command_s
            
    '''
    入口方法go
    '''
    def go(self):
        htmls = self.fetch_content()
        anchors = self.analysis(htmls)
        anchors = list(self.refine(anchors))
        command_s = self.show(anchors)
        return command_s


spider4 = Spider4()
temp4 = spider4.go()
text2 = [] #用于接收岗位要求
str1 = '' #用于接收岗位要求并转化为字符串
for t4 in temp4:
    spider3 = Spider3(t4)
    temp3 = spider3.go()
    for t3 in temp3[2:]: # 前两条列表网址不一致，舍去
        t3 = t3.replace("\\","")
        spider = Spider(t3)
        text1 = spider.go() #将岗位要求传出至text1
        text2.append(text1) #将岗位要求传出至text2

'''
对岗位要求进行文字处理
'''
for i in text2:
    str1 = str1+str(i)
str1 = str(str1.replace('[', ''))
str1 = str(str1.replace(']', ''))
str1 = str(str1.replace('\n', ''))
str1 = str(str1.replace('<span>', ''))
str1 = str(str1.replace('</span>', ''))

dict1 = {}
dict2 = {}
'''
统计7个字符的工作要求的出现次数
'''
for i in range(0, len(str1)-6):
    list1 = dict1.keys()
    two = str1[i]+str1[i+1]+str1[i+2]+str1[i+3]+str1[i+4]+str1[i+5]+str1[i+6]
    if two in list1:
        dict1[two] = dict1[two]+1
    else:
        dict1[two] = 1

print('按照键值对的形式，展示每个工作要求的数量：', '\n', dict1)
print()
print()
print()
for i in range(0, 100):
    key1 = max(dict1, key=dict1.get)
    dict2[key1] = dict1[key1]
    del dict1[key1]

print('只展示出现次数最多的前100个工作要求和对应的数量：', '\n', dict2)


'''
Python
总计433条数据
数据库（332次），SQL（258次），Linux（176次），Django（151次），Flask（103次），
Redis（101次），MongoDB（75次）
'''
