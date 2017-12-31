from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta
from data import enum_model
import os

class Station:
    '''
    海洋站model
    '''
    def __init__(self,name,code,datatype):
        '''

        :param name: 海洋站名字
        :param code: 对应的站代码（5位数字）
        :param datatype: 要素字典
        '''
        self.stationname=name
        self.stationcode=code
        self.datatype=datatype

class DateTime:
    '''
    时间model
    '''
    def __init__(self,start,finish):
        '''

        :param start:起始时间
        :param finish:终止时间
        '''
        self.start=start
        self.finish=finish

import os

class MarinData:
    '''
    海洋数据
    '''
    def __init__(self,path,filename,type,element):
        '''

        :param path:路径
        :param type:种类
        '''
        self.path=path
        self.filename=filename
        self.type=type
        self.element=element

    @property
    def fullname(self):
        '''
        全路径名称
        :return:
        '''
        return os.path.join(self.path,self.filename)

    @property
    def targetdate(self):
        '''
        根据path与filename获取指定时间
        eg:
        path:
            E:\03协同开发\99学习\05数据分析\网课源码\learn_sourcecode_DataAnalysis\codes_bymyself\data\ceshi\perclock\2017\11\01
        filename:
            SL1101.11754
        :return:
        '''

        '''
        通过正则匹配时间的思路：
            S1、先将path中的\或更多的\替换为一个\
            1、找到perclock\ 与后面的\之间的 作为 year
            2、year 之后的\ \ 之间的 作为 month
            3、month 之后的 \ \ 之间的作为 day
        '''
        index= self.path.index('perclock')
        per_len=len('perclock')
        # \\2017\\11\\01\\SL1101.11754
        ext_str=self.path[index+per_len:]
        # 根据 \\ 切分为集合
        # ['', '2017', '11', '01', 'SL1101.11754']
        # 注意win与mac下的分隔符不同
        # 此处需要获取系统的分隔符
        separator= os.sep
        list_split=ext_str.split(separator)
        year=int(list_split[1])
        month=int(list_split[2])
        day=int(list_split[3])
        # 注意创建时间对象时，只能传入int类型
        return datetime(year,month,day)