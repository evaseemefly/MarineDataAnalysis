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
from conf import settings
import numpy as np
import pandas as pd
import datetime
from enum import Enum
from abc import ABCMeta, abstractmethod



class ReadTimeData:
    '''
    by zhiw
    '''
    def __init__(self):
        pass

class Station:
    '''
    海洋站
    '''
    def __init__(self,name,code):
        self.name=name
        self.code

class BaseData:
    '''
    水文气象的父类，
    有一个抽象方法getTargetMonthAllDaysList
    '''
    def __init__(self,dirpath,station,targetdate):
        self.dirpath=dirpath
        self.station=station
        self.targetdate=targetdate


    @abstractmethod
    def getTargetMonthAllDaysList(self,temp_date):
        '''
        根据传入的时间，返回该时间对应的月数据
        :return:
        '''
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

    def getbetweenDays(start, finish,format_date='%Y%m%d'):
        date_list = []
        # start_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        # finish_date = datetime.datetime.strptime(finish, '%Y-%m-%d %H:%M:%S')
        start_date=start
        finish_date=finish
        while start_date <= finish_date:
            #"%Y%m%d%H"
            #format_date= kwargs['format_date']
            date_str = start_date.strftime(format_date)
            date_list.append(date_str)
            start_date += datetime.timedelta(1)
            # print(date_list)
        return date_list




    def getNextMonth1stDay(temp_date):
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

    def getThisMonthEndDay(self,temp_date):
        '''
        获取传入日期的当月的最后一天
        :param temp_date:
        :return:
        '''
        now_date = temp_date
        year = now_date.year
        month = now_date.month
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        next_month=datetime.datetime(year,month,1)
        target_date=next_month+ datetime.timedelta(-1)
        return target_date

    def validate(self):
        '''
        数据验证
        :return:
        '''
        pass

    class MeteorologyData(BaseData):
        '''
        气象数据
        气象数据格式是前一天21点-当日的20点
        我的思路，气象数据与水文数据类中都有getTargetMonthAllDaysList这个方法
        '''


        def getTargetMonthAllDaysList(self, temp_date):
            '''
            获取指定指定月份的所有天的集合
            :param temp_date:
            :return:返回当前日期的当前月第一天到下月第一天的days list
            '''
            # 获得当月的起始时间
            start = temp_date
            # start = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            # 获取下个月的首日

            finish = PerclockData.getNextMonth1stDay(start)
            days = PerclockData.getbetweenDays(start, finish,format_date='%Y%m%d')
            return days
            # print(start)

    class HydrologyData(BaseData):
        '''
        水文数据
        水文的数据格式本身就是00-23的格式
        '''
        def __init__(self,dirpath,station,targetdata):
            # self.dirpath=dirpath
            super(PerclockData.HydrologyData, self).__init__(dirpath,station,targetdata)
            # self.dirpath=dirpath
            # super(HydrologyData, self).__init__(dirpath)
            # BaseData.__init__(self,dirpath)
            # super.__init__(self,dirpath)

        def columns(self,temp_date):
            '''

            :param temp_date:
            :return:
            '''
            arr_str = [temp.zfill(2) for temp in np.arange(24).astype(str).tolist()]
            arr_str.insert(0, 'date')
            arr_str.append('max')
            arr_str.append('min')
            return arr_str



        def getTargetDayData(self,temp_date):
            '''
            读取指定日期对应的文件，读取其中的数据为dataframe
            :param temp_date:
            :return:
            '''
            # 目标文件的全名称
            # targetFileFullName="%s/wt%s.%s"%(BaseData.dirpath,temp_date.strftime("%m%d"),PerclockData.station)
            targetFileFullName = "%s/wt%s.%s" % (self.dirpath, temp_date.strftime("%m%d"), PerclockData.station)
            result_wt = pd.read_table(targetFileFullName, sep='\s+', names=self.columns(temp_date))
            print(result_wt)
            pass

        def getTargetMonthAllDaysList(self, temp_date):
            '''
            获取指定指定月份的所有天的集合
            :param temp_date:
            :return:返回当前日期的当前月第一天到下月第一天的days list
            '''
            # 获得当月的起始时间
            start = temp_date
            # start = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            # 获取下个月的首日
            finish = PerclockData.getNextMonth1stDay(start)
            days = PerclockData.getbetweenDays(start, finish)
            return days
            # print(start)



def main():
    perclock= PerclockData('wer','123')
    now=datetime.datetime(2017,11,29)
    # perclock.HydrologyData(settings.BASE_DIR+"/data")
    # hydata=PerclockData.HydrologyData(settings.BASE_DIR+"/data")
    hydata = perclock.HydrologyData(settings.BASE_DIR + "/data")
    hydata.getTargetDayData(now)
    print(hydata.getTargetMonthAllDaysList(now))
   # perclock.getNextMonth1stDay(now)

if __name__ == "__main__":
    main()












            