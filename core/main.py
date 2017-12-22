
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
    station=model.Station("ceshi","11754","")

    date_str = '2017-11-29'
    # date_target=datetime.datetime.strptime(date_str,'%Y-%m-%d')
    target_date = datetime.strptime(date_str, '%Y-%m-%d')

    # en=MarineData.PerclockData(station,target_date)
    en = MarineData.PerclockData(station, target_date)

    environment=OperEnvironment(en.build_Data(enum_model.DataType.Hydrology,settings.SOURCE_PATH))
    environment.run()
    pass

if __name__=='__main__':
    main()

