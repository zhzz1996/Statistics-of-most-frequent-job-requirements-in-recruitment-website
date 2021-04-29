'''
本模块的任务是获取求职列表
'''

from spider4 import Spider4
import re #引入正则模块
from urllib import request #引入数据请求模块

class Spider3():

    def __init__(self, url):
            self.url = url

    root_pattern = '"job_href":"([\s\S]*?)","job_name"' #相关信息正则表达式-类变量
   
    '''
    抓取数据方法fetch_content
    '''
    def fetch_content(self):
        r = request.urlopen(self.url) #调用request的urlopen方法
        htmls = r.read()
        htmls = str(htmls,encoding='gbk',errors='ignore')
        return htmls
    
    '''
    数据分析方法analysis
    '''
    def analysis(self, htmls):
        root_html = re.findall(Spider3.root_pattern, htmls)
        return root_html

    def go(self):
        htmls = self.fetch_content()
        root_html = self.analysis(htmls)
        return root_html


