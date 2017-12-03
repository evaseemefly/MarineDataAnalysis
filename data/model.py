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