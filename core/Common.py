from datetime import datetime
from datetime import timedelta
from data import enum_model

class DateHelper:
    def __init__(self,date_str):
        # 输入日期字符串并转换为datetime类型
        self.targetdate=datetime.strptime(date_str,'%Y-%m-%d-%H-%M')

    def date_factory(self,data_type):
        '''
        日期工厂处理水文及气象两种类型的时间问题
        :param data_type:
        :return:
        '''
        # 气象要素
        if data_type==enum_model.DataType.Meteorology:
            pass
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
        def __init__(self,date):
            self.date=date
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




