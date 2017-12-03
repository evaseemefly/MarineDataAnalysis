'''
思路：
分钟和整点数据均有:
-1 获取文件全路径集合的方法，统一为getTargetFullNameList
-2 读取文件中内容的方式，统一命名为readData
-3 验证数据内容的方法，统一命名为validate
'''
import os
import data.model
from pandas import Series,DataFrame
import numpy as np
import pandas as pd

class ReadTimeData:
    '''
    by zhiw
    '''
    def __init__(self):
        pass

class PerclockData:
    '''
    by casablanca
    '''
    def __init__(self,station,date):
        '''
        传入海洋站 及 日期 model
        :param station:
        :param date:
        '''
        self.station=station
        self.date=date
        pass

    def getTargetFullNameList(self):
        '''
        根据海洋站名称获取指定海洋站的规定时间范围内的文件全路径集合
        :return:
        '''
        pass

    def readData(self,targetpath):
        '''
        读取数据
        读取该文件中的整点数据，并以dataframe的类型返回
        :return:
        '''

        # 判断指定文件是否存在
        if os.path.exists(targetpath):
            # 存在则打开
            result= pd.read_table(targetpath,sep='\s+')
        pass

    def validate(self):
        '''
        数据验证
        :return:
        '''
        pass