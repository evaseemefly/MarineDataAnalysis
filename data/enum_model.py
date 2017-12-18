from enum import Enum

class DataType(Enum):
    '''
    数据类型的枚举
    0：气象
    1：水文
    '''
    Meteorology=0
    Hydrology=1