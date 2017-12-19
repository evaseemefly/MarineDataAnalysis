from datetime import datetime
from datetime import timedelta
from data import enum_model

from pandas import Series,DataFrame
import numpy as np
import pandas as pd

class DateHelper:
    def __init__(self,date_str):
        # 输入日期字符串并转换为datetime类型
        self.targetdate=datetime.strptime(date_str,'%Y-%m-%d-%H-%M')

    def date_factory(self,data_type,date):
        '''
        日期工厂处理水文及气象两种类型的时间问题
        :param data_type:
        :return:
        '''
        # 气象要素
        if data_type==enum_model.DataType.Meteorology:
            return self.Hydrology_date(date)
        # 水文要素
        elif data_type==enum_model.DataType.Hydrology:
            pass


    class Meteorology_date:
        '''
        气象要素时间处理
        '''
        def __init__(self,date):
            pass

    class Hydrology_date:
        '''
        水文要素时间处理
        '''
        def __init__(self,date,type_str):
            self.date=date
            self.date_type=type_str
            self.result
            self.columns
            self.list_date
            # 起始及终止时间
            # 不使用以下的方式
            # self.start_date
            # self.end_date

        @property
        def start_date(self):
            '''
            根据当前的时间计算起始时间
            :return:
            '''
            return datetime(self.date.year,self.date.month,self.date.day)


        @property
        def end_date(self):
            '''
            根据当前的时间计算终止时间
            :return:
            '''
            return self.start_date+timedelta(hours=23)

        @property
        def list_date(self):
            '''
            获取日期时间列表
            00-23时
            :return:
            '''
            if self.list_date is None:
                self.list_date=pd.date_range(self.start_date, periods=24, freq='H')
            return self.list_date



        # 以下内容移到 core.MarinData.PerclockData.HydroplogyData中
        # def __read_table(self,path):
        #     self.result=pd.read_table(path,sep='\s+',names=self.table_columns)

        # @property
        # def table_columns(self):
        #     if self.columns is None:
        #         arr_temp = np.arange(24).tolist()
        #         arr_str = [temp.zfill(2) for temp in np.arange(24).astype(str).tolist()]
        #         arr_str.insert(0, 'date')
        #         arr_str.append('max')
        #         arr_str.append('min')
        #     return self.columns
        #
        #
        # def getData(self):
        #     '''
        #     获取数据：
        #     具体步骤如下：
        #     1 生成时间list
        #     2 读取指定文件
        #     3 对读取后的dataframe进行转换
        #     4 将最终结果返回
        #     :return:
        #     '''
        #     self.__read_table()
        #     # 删除数据的date列
        #     del self.result['date']
        #     #转置
        #     self.result= self.result.T
        #     # 切片获取0-23点的数据，去掉min与max
        #     self.result = self.result[:-2]
        #     # 对df的index赋值
        #     self.result.index=self.list_date
        #     # 对df的columns赋值
        #     # columns就是at hu 等等
        #     self.result.columns=[self.date_type]
        #     return self.result




