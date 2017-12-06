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
import datetime
from enum import Enum

class DataType(Enum):
    '''
    数据类型的枚举
    0：气象
    1：水文
    '''
    Meteorology=0
    Hydrology=1

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

    def getbetweenDays(self,start, finish):
        date_list = []
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        finish_date = datetime.datetime.strptime(finish, '%Y-%m-%d %H:%M:%S')
        while start_date <= finish_date:
            date_str = start_date.strftime("%Y%m%d%H")
            date_list.append(date_str)
            start_date += datetime.timedelta(1)
            # print(date_list)
        return date_list




    def getNextMonth1stDay(self,temp_date):
        '''
        获取传入时间的下个月的第一天的时间
        :param temp_date: 当前时间
        :return:下个月的第一天的时间
        '''
        now_date=temp_date
        year=now_date.year
        month=now_date.month
        if month==12:
            month=1
            year+=1
        else:
            month+=1
        target_date=datetime.datetime(year,month,1)
        return target_date
        # print(target_date)

    def validate(self):
        '''
        数据验证
        :return:
        '''
        pass

    class MeteorologyData:
        '''
        气象数据
        气象数据格式是前一天21点-当日的20点
        '''
        def __init__(self):
            pass

        def getTargetMonthAllDaysList(self, temp_date, datatype):
            '''
            获取指定指定月份的所有天的集合
            :param temp_date:
            :return:返回当前日期的当前月第一天到下月第一天的days list
            '''
            # 获得当月的起始时间
            start = temp_date
            # start = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            # 获取下个月的首日
            finish = self.getNextMonth1stDay(start)
            days = self.getbetweenDays(start, finish)
            return days
            # print(start)

    class HydrologyData:
        '''
        水文数据
        水文的数据格式本身就是00-23的格式
        '''
        def __init__(self):
            pass

        def getTargetMonthAllDaysList(self, temp_date, datatype):
            '''
            获取指定指定月份的所有天的集合
            :param temp_date:
            :return:返回当前日期的当前月第一天到下月第一天的days list
            '''
            # 获得当月的起始时间
            start = temp_date
            # start = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            # 获取下个月的首日
            finish = self.getNextMonth1stDay(start)
            days = self.getbetweenDays(start, finish)
            return days
            # print(start)



def main():
    perclock= PerclockData('wer','123')
    now=datetime.datetime(2017,11,1)
    perclock.getNextMonth1stDay(now)

if __name__=='__main__':
    main()