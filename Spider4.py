'''
本模块的任务是获取求职页面
'''

import re #引入正则模块
from urllib import request #引入数据请求模块

class Spider4():
    def go(self):
        wangzhi = []
        for i in range(2): #选取前2页
            wz = 'https://search.51job.com/list/030000%252c180200%252c080200%252c020000,000000,0000,00,9,99,python,2,'+str(i)+'.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
            wangzhi.append(wz)
        return wangzhi
