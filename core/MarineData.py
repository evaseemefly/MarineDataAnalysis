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
import re
from enum import Enum
from abc import ABCMeta, abstractmethod
from core import Common
from data import enum_model
from data import model


# 注意此处\D是非数字！
re_match=[r'^WL\d{4}.\d{5}$',r'^WS\d{4}.\d{5}$',r'^WV\d{4}.\d{5}$']

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
        self.result=None


    # @abstractmethod
    # def getDataResult(self):
    #     '''
    #     根据传入的时间，返回该时间对应的月数据
    #     :return:
    #     '''
    #     pass

    def getDataResult(self):
        """
         获取数据：
        具体步骤如下：
        1 生成时间list
        2 读取指定文件
        3 对读取后的dataframe进行转换
        4 将最终结果返回

        存在的设计问题：
        由于是外侧类的工厂方法调用，而外侧的类中getmatchingFiles方法是生成该月的所有匹配文件集合
        :return:
        """
        date_helper = Common.DateHelper(self.targetdate)
        temp_date = date_helper.date_factory(enum_model.DataType.Meteorology)

        isOK=self.getTargetDayData()
        # 若读取时出错时直接跳出
        if isOK==False:
            return
        if self.element.lower() != 'ws':
            # self.__read_table()
            # 删除数据的date列
            del self.result['date']
            # 转置
            self.result = self.result.T
            # 切片获取0-23点的数据，去掉min与max
            self.result = self.result[:-2]
            # 对df的index赋值
            self.result.index = temp_date.list_date
            # 对df的columns赋值
            # columns就是at hu 等等
            self.result.columns = [self.element]
        # 注意风向风速的要特殊处理！！！
        elif self.element.lower() == 'ws':
            # 获取第一行（相当于是列头）
            columns = self.result.columns
            # 获取剔除第一个日期之外的其他值
            self.result = pd.DataFrame(columns)[1:]
            # 修改形状
            self.result = pd.DataFrame(self.result.values.reshape((24, 2)))
            self.result.index = temp_date.list_date
            self.result.columns = ['WD', 'WS']
        return self.result

    def getTargetDayData(self):
        """
        读取指定日期对应的文件，读取其中的数据为dataframe
        :param temp_date:
        :return:
        """
        '''
        读取指定日期对应的文件，读取其中的数据为dataframe
        :param temp_date:
        :return:
        '''
        isOK=False
        # 目标文件的全名称
        # targetFileFullName = "%s/wt%s.%s" % (self.dirpath, temp_date.strftime("%m%d"), self.station)
        targetFileFullName = "%s" % (self.dirpath)
        # targetFileFullName = "%s/wt%s.%s" % (self.dirpath, temp_date.strftime("%m%d"), self.outter.station)
        # ！！！！注意使用下面的方式 若路径中存在中文，则会出现问题
        # self.result = pd.read_table(targetFileFullName, sep='\s+', names=self.__columns)
        # 改为此种方式不会有问题
        f = open(targetFileFullName)
        # 注意此处也要加入判断，因为ws的数据在读取数据时与其他数据也略有不同，不需要指定columns

        if self.element.lower() != "ws":
            # 注意此处有问题，父类无法直接调用子类的私有属性或方法
            # 将子类中的属性修改为公开的
            # columns=self.__columns
            columns = self.columns
            try:

                self.result = pd.read_csv(f, sep='\s+', names=columns)
                isOK=True
            except UnicodeDecodeError:
                print("编码错误")
            except Exception:
                print("未知错误")
        elif self.element.lower() == "ws":
            try:
                self.result = pd.read_csv(f, sep='\s+')
                isOK = True
            except UnicodeDecodeError:
                print("编码错误")
            except Exception:
                print("未知错误")
            # print(self.result)
        return isOK


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

    # def build_Data(self, data_type, path):
    def build_Data(self,path):
        '''
        使用工厂方法（现已修改）
        根据报文类型（水文、气象）以及根目录：
            1、获取所有匹配的文件全目录集合
            2、
        :param data_type:
        :return:
        '''

        # stations_list= self.getmatchingFiles(os.path.join(path,self.station.stationname),self.date)
        # 先获取文件目录
        # 注意此处获取的文件全路径时传入的时间的当月的全部文件
        files,ignorefiles=self.getmatchingFiles(os.path.join(path,self.station.stationname),self.date)
        # 创建空的dataframe
        # 注意此处与HydrologyData.getDataResult中均用到Common.DateHelper(self.date)！！！！！需要再修改
        date_helper = Common.DateHelper(self.date)
        temp_date = date_helper.date_factory(enum_model.DataType.Hydrology)

        df_all= self.__creatNaDataframe(temp_date.list_date_allmonth)
        # temp_perclock_data=None
        '''
        下面重新修改
            1 遍历文件集合
            2 对当前的文件根据其类型实例化对应的内部类
            3 调用getDataResult方法
        '''
        for temp_file in files:
            # 遍历文件名集合，并对其分类
            # 使用工厂方式创建的水文和气象数据对象均要实现getDataResult方法
            temp_data_hy=None
            temp_data_me = None
            # 此处不再使用判断传入的类型，改为遍历的水文、气象两种类型的数据
            # for temp_enum in enum_model.DataType:
            print("正在录入%s"%temp_file.fullname)
            temp_data_hy = self.HydrologyData(temp_file.fullname, self.station, temp_file.targetdate, temp_file.element)
            result_hy = temp_data_hy.getDataResult()
            if result_hy is None:
                continue
            df_all = df_all.combine_first(result_hy)

            temp_data_me = self.MeteorologyData(temp_file.fullname, self.station, temp_file.targetdate, temp_file.element)
            result_me = temp_data_me.getDataResult()
            if result_me is None:
                continue
            df_all = df_all.combine_first(result_me)
            print("录入成功")
            # if data_type is enum_model.DataType.Hydrology:
            #     # 此处有问题，遍历的file对象应该是对每个file对象获取其对应的时间，而不能使用self.date
            #     temp_data= self.HydrologyData(temp_file.fullname,self.station,temp_file.targetdate,temp_file.element)
            # elif data_type is enum_model.DataType.Meteorology:
            #     temp_data= self.MeteorologyData(temp_file.fullname,self.station,temp_file.targetdate,temp_file.element)
            # result=temp_data.getDataResult()
            # df_all=df_all.combine_first(result)
            # temp_perclock_data.getDataResult()
        return df_all

    def __creatNaDataframe(self,date_list):
        columns = ['DT', 'WT', 'SL', 'WL', 'AT', 'BP', 'RN', 'VB', 'HU', 'WD', 'WS']
        df_all = pd.DataFrame(columns=columns, index=date_list)
        return df_all

    def getmatchingFiles(self,path,target_date):
        """[summary]
        根据时间获取该目录下的该月的所有整点报文的全路径
         return model.Station
        [description]
        
        Arguments:
            path {[type]} -- [description] 到海洋站一级的目录
        """
        files_list = []
        ignorefiles_list = []
        # 当前路径下的目录
        year=str(target_date.year)
        month=str(target_date.month)
        # year='2017'
        # month='11'
        # start='01'
        # end='30'
        '''
        在mac下：
        path：/Users/liusihan/Documents/GitHub/learn_sourcecode_DataAnalysis/codes_bymyself/data/sanya/perclock/
        source_dir：
        'perclock'
        '''
        # 获取数据种类及水文气象对应的分类
        dict_marindata=settings.DATA_TYPE
        path=os.path.join(path,"perclock")

        source_dir=os.listdir(path)
        if year in source_dir:
            year_dir=os.path.join(path,year)
            month_dir=os.listdir(year_dir)        
            if month in month_dir:
                targetpath=os.path.join(year_dir,month)
                '''
                targetpath目录是到月的目录
                月的目录下还有日的文件夹
                '''
                for root, dirs, files in os.walk(targetpath):
                    for temp_dir in dirs:
                        temp_targetpath=os.path.join(targetpath,temp_dir)
                        for root,dirs,files in os.walk(temp_targetpath):
                            # if len(dirs)==0:
                            for temp_file in files:
                                ''' 
                                注意追加时不是所有的文件名都要追加
        
                                '''
                                # 根据文件名判断文件的水文气象分类

                                str_file=temp_file.upper()
                                # 肯定是大写的
                                res_match_type = re.match('[a-zA-Z]{2}', str_file)
                                if res_match_type!=None:
                                    # 使用group匹配正则的匹配值
                                    res_match_type = res_match_type.group()
                                    # 从字典中找到对应的
                                    data_value= settings.DATA_TYPE[res_match_type]
                                    # result = 5 > 3?1: 0
                                    # 注意py中不支持三元运算符
                                    data_value=enum_model.DataType.Hydrology if data_value == 'H' else enum_model.DataType.Meteorology
                                    # data_value=(data_value=='H'? enum_model.DataType.Hydrology:enum_model.DataType.Meteorology)
                                    is_matching=False
                                    marinData_model = model.MarinData(root,temp_file, data_value,res_match_type)
                                    #marinData_model=model.MarinData(os.path.join(root, temp_file), data_value)
                                    # 有符合正则条件的放入忽略集合中
                                    for temp_match in re_match:
                                        res_match=re.match(temp_match,str_file)
                                        if res_match!=None:
                                            is_matching=True

                                            ignorefiles_list.append(marinData_model)
                                            print("****%s已追加至忽略集合中"%marinData_model.fullname)
                                            break
                                        # 不匹配的才放入文件集合中
                                    if is_matching==False:
                                       files_list.append(marinData_model)
                                       print("%s已追加"%marinData_model.fullname)
                            print("-----------")
        return files_list,ignorefiles_list

    def getTargetFullNameList(self,dirpath):
        '''
        根据海洋站名称获取指定海洋站的规定时间范围内的文件全路径集合
        根据传入的根目录获取指定海洋站的，在指定时间范围内的文件路径集合
        :return:
        '''
        elements=['AT','BP','HU','RN','SL','WL','WS','WT']

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

        @property
        def columns(self):
            '''

            :param temp_date:
            :return:
            '''
            yesterday = np.arange(21, 24).astype(str)
            today = np.arange(0, 21).astype(str)
            # 气象时间list
            meteorology_date = np.hstack((yesterday, today)).tolist()
            meteorology_date.insert(0, 'date')
            meteorology_date.append('max')
            meteorology_date.append('min')
            return meteorology_date



        def __init__(self, dirpath, station, targetdata,element):
            super(PerclockData.MeteorologyData, self).__init__(dirpath, station, targetdata)
            self.element = element

        # def __getTargetDayData(self):
        #     """
        #     读取指定日期对应的文件，读取其中的数据为dataframe
        #     :param temp_date:
        #     :return:
        #     """
        #     '''
        #     读取指定日期对应的文件，读取其中的数据为dataframe
        #     :param temp_date:
        #     :return:
        #     '''
        #     # 目标文件的全名称
        #     # targetFileFullName = "%s/wt%s.%s" % (self.dirpath, temp_date.strftime("%m%d"), self.station)
        #     targetFileFullName="%s"%(self.dirpath)
        #     # targetFileFullName = "%s/wt%s.%s" % (self.dirpath, temp_date.strftime("%m%d"), self.outter.station)
        #     # ！！！！注意使用下面的方式 若路径中存在中文，则会出现问题
        #     # self.result = pd.read_table(targetFileFullName, sep='\s+', names=self.__columns)
        #     # 改为此种方式不会有问题
        #     f = open(targetFileFullName)
        #     # 注意此处也要加入判断，因为ws的数据在读取数据时与其他数据也略有不同，不需要指定columns
        #
        #     if self.element.lower()!="ws":
        #         self.result=pd.read_csv(f, sep='\s+', names=self.__columns)
        #     elif self.element.lower()=="ws":
        #         self.result = pd.read_csv(f, sep='\s+')
        #     # print(self.result)


        '''
        水文气象的两个子类的getDataResult方法均写在父类BaseData中
        '''
        # def getDataResult(self):
        #     """
        #      获取数据：
        #     具体步骤如下：
        #     1 生成时间list
        #     2 读取指定文件
        #     3 对读取后的dataframe进行转换
        #     4 将最终结果返回
        #
        #     存在的设计问题：
        #     由于是外侧类的工厂方法调用，而外侧的类中getmatchingFiles方法是生成该月的所有匹配文件集合
        #     :return:
        #     """
        #     date_helper = Common.DateHelper(self.targetdate)
        #     temp_date = date_helper.date_factory(enum_model.DataType.Meteorology)
        #
        #     self.getTargetDayData()
        #     if self.element.lower() != 'ws':
        #         # self.__read_table()
        #         # 删除数据的date列
        #         del self.result['date']
        #         # 转置
        #         self.result = self.result.T
        #         # 切片获取0-23点的数据，去掉min与max
        #         self.result = self.result[:-2]
        #         # 对df的index赋值
        #         self.result.index = temp_date.list_date
        #         # 对df的columns赋值
        #         # columns就是at hu 等等
        #         self.result.columns = [self.element]
        #     # 注意风向风速的要特殊处理！！！
        #     elif self.element.lower() == 'ws':
        #         # 获取第一行（相当于是列头）
        #         columns = self.result.columns
        #         # 获取剔除第一个日期之外的其他值
        #         self.result = pd.DataFrame(columns)[1:]
        #         # 修改形状
        #         self.result = pd.DataFrame(self.result.values.reshape((24, 2)))
        #         self.result.index = temp_date.list_date
        #         self.result.columns = ['WD', 'WS']
        #     return self.result


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
        """[summary]
        水文数据
        水文的数据格式本身就是00-23的格式
        [description]
        """
        '''
        水文数据
        水文的数据格式本身就是00-23的格式
        '''

        def __init__(self, dirpath, station, targetdata,element):
        # def __init__(self,outter,dirpath,station,targetdata):
            # self.dirpath=dirpath
            super(PerclockData.HydrologyData, self).__init__(dirpath,station,targetdata)
            self.element=element
            # super(PerclockData.HydrologyData, self).__init__(outter, dirpath, station, targetdata)
            # self.outter=outter
            # self.dirpath=dirpath
            # super(HydrologyData, self).__init__(dirpath)
            # BaseData.__init__(self,dirpath)
            # super.__init__(self,dirpath)

        @property
        def columns(self):
            '''

            :param temp_date:
            :return:
            '''
            arr_str = [temp.zfill(2) for temp in np.arange(24).astype(str).tolist()]
            arr_str.insert(0, 'date')
            arr_str.append('max')
            arr_str.append('min')
            return arr_str

        # def __getTargetDayData(self):
        #     """
        #     读取指定日期对应的文件，读取其中的数据为dataframe
        #     :param temp_date:
        #     :return:
        #     """
        #     '''
        #     读取指定日期对应的文件，读取其中的数据为dataframe
        #     :param temp_date:
        #     :return:
        #     '''
        #     # 目标文件的全名称
        #     # targetFileFullName = "%s/wt%s.%s" % (self.dirpath, temp_date.strftime("%m%d"), self.station)
        #     targetFileFullName="%s"%(self.dirpath)
        #     # targetFileFullName = "%s/wt%s.%s" % (self.dirpath, temp_date.strftime("%m%d"), self.outter.station)
        #     # ！！！！注意使用下面的方式 若路径中存在中文，则会出现问题
        #     # self.result = pd.read_table(targetFileFullName, sep='\s+', names=self.__columns)
        #     # 改为此种方式不会有问题
        #     f = open(targetFileFullName)
        #     # 注意此处也要加入判断，因为ws的数据在读取数据时与其他数据也略有不同，不需要指定columns
        #
        #     if self.element.lower()!="ws":
        #         self.result=pd.read_csv(f, sep='\s+', names=self.__columns)
        #     elif self.element.lower()=="ws":
        #         self.result = pd.read_csv(f, sep='\s+')
        #     # print(self.result)


        # 不在使用此方法了
        # def getTargetMonthAllDaysList(self, temp_date):
        #     '''
        #     获取指定指定月份的所有天的集合
        #     :param temp_date:
        #     :return:返回当前日期的当前月第一天到下月第一天的days list
        #     '''
        #     # 获得当月的起始时间
        #     start = temp_date
        #     # start = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        #     # 获取下个月的首日
        #     finish = PerclockData.getNextMonth1stDay(start)
        #     days = PerclockData.getbetweenDays(start, finish)
        #     return days
        #     # print(start)


        '''
         水文气象的两个子类的getDataResult方法均写在父类BaseData中
         '''
        # def getDataResult(self):
        #     """
        #      获取数据：
        #     具体步骤如下：
        #     1 生成时间list
        #     2 读取指定文件
        #     3 对读取后的dataframe进行转换
        #     4 将最终结果返回
        #
        #     存在的设计问题：
        #     由于是外侧类的工厂方法调用，而外侧的类中getmatchingFiles方法是生成该月的所有匹配文件集合
        #     :return:
        #     """
        #     date_helper = Common.DateHelper(self.targetdate)
        #     temp_date=date_helper.date_factory(enum_model.DataType.Hydrology)
        #
        #     self.getTargetDayData()
        #     if self.element.lower()!='ws':
        #         # self.__read_table()
        #         # 删除数据的date列
        #         del self.result['date']
        #         #转置
        #         self.result= self.result.T
        #         # 切片获取0-23点的数据，去掉min与max
        #         self.result = self.result[:-2]
        #         # 对df的index赋值
        #         self.result.index=temp_date.list_date
        #         # 对df的columns赋值
        #         # columns就是at hu 等等
        #         self.result.columns=[self.element]
        #     # 注意风向风速的要特殊处理！！！
        #     elif self.element.lower()=='ws':
        #         # 获取第一行（相当于是列头）
        #         columns = self.result.columns
        #         # 获取剔除第一个日期之外的其他值
        #         self.result = pd.DataFrame(columns)[1:]
        #         # 修改形状
        #         self.result = pd.DataFrame(self.result.values.reshape((24, 2)))
        #         self.result.index = temp_date.list_date
        #         self.result.columns = ['WD', 'WS']
        #     return self.result



# def main():
#     perclock= PerclockData('wer','123')
#     now=datetime.datetime(2017,11,29)
#     # perclock.HydrologyData(settings.BASE_DIR+"/data")
#     # hydata=PerclockData.HydrologyData(settings.BASE_DIR+"/data")
#     hydata = perclock.HydrologyData(settings.BASE_DIR + "/data")
#     hydata.getTargetDayData(now)
#     print(hydata.getTargetMonthAllDaysList(now))
#    # perclock.getNextMonth1stDay(now)
#
# if __name__ == "__main__":
#     main()












            