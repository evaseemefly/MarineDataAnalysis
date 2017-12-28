import logging
import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 海洋站的原始路径
# mac 上的地址
# SOURCE_PATH=r"/Users/liusihan/Documents/GitHub/learn_sourcecode_DataAnalysis/codes_bymyself/data/"
SOURCE_PATH=r"/Users/liusihan/Documents/重要测试数据/sanya"
# SOURCE_PATH=r"E:\03协同开发\单位海洋站数据分析\data"

# 输出的路径
# TARGET_PATH=r"E:\03协同开发\单位海洋站数据分析\result\201711.csv"
TARGET_PATH=r"/Users/liusihan/Documents/重要测试数据/result/201711.csv"
# 海洋站 字典
# 类似django中的settings中的DATABASE
STATIONS={
    '07422':{
        'NAME':'小长山',
        'TYPE':'wt,sl,wl,at,bp,hu,rn,ws'
    },
    '07423':{
        'NAME':'千里岩',
        'TYPE':'wt,sl,wl,at,bp,hu,rn,ws'
    },

}

'''
  水文：H
  气象：M
'''
DATA_TYPE={
    'WT':'H',
    'SL':'H',
    'WL':'H',
    'WS':'H',
    'AT':'M',
    'BP':'M',
    'HU':'M',
    'RN':'M',
}

# 日志的相关配置
LOG_LEVEL=logging.INFO

LOG_TYPES={
    'existDirLog':'currentdirlist.log',
    'copyDirLog':'copyInfo.log',
    'myLog':'console.log'
    }