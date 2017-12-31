
import os
# import bin.MarineData
from core import MarineData
from data import model
from datetime import datetime
from data import enum_model
from datetime import timedelta
from conf import settings

from pandas import Series,DataFrame
import numpy as np
import pandas as pd

# 当前项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class OperEnvironment:
    def __init__(self,factory):
        '''
        传入一个工厂
        :param factory:
        '''
        self.marineData=factory
        pass

    def run(self):

        self.marineData.getDataResult()


def main():
    '''
    主函数
    :return:
    '''
    # 1、根据配置文件或输入选择当前是读取整点还是分钟的数据
    #
    print(BASE_DIR)
    station=model.Station("sanya","11754","")

    date_str = '2017-11-29'
    # date_target=datetime.datetime.strptime(date_str,'%Y-%m-%d')
    target_date = datetime.strptime(date_str, '%Y-%m-%d')

    # 处理12个月的数据
    months_list=pd.date_range(datetime(target_date.year,1,1),periods=12,freq='M')
    for temp_date in months_list:
        # en=MarineData.PerclockData(station,target_date)
        en = MarineData.PerclockData(station, temp_date)

        # 不再需要传入报文类型——2017 12 27
        # df_all= en.build_Data(enum_model.DataType.Hydrology,settings.SOURCE_PATH)
        df_all = en.build_Data(settings.SOURCE_PATH)


        target_csv=os.path.join(settings.TARGET_DIR_PATH,"%s%s_%s.csv"%(temp_date.year,temp_date.month,station.stationname))
        # if df_all!=None:
        # df_all.to_csv(settings.TARGET_PATH)
        fp = open("target_csv", 'w')
        fp.close()
        # os.tempname(target_csv)
        df_all.to_csv(target_csv)

    # 不使用此种方式
    # environment=OperEnvironment(en.build_Data(enum_model.DataType.Hydrology,settings.SOURCE_PATH))
    # environment.run()
    pass

if __name__=='__main__':
    main()

