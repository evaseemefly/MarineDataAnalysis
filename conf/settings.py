import logging
import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 海洋站的原始路径
SOURCE_PATH=r""
# 输出的路径
TARGET_PATH=r""

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

# 日志的相关配置
LOG_LEVEL=logging.INFO

LOG_TYPES={
    'existDirLog':'currentdirlist.log',
    'copyDirLog':'copyInfo.log',
    'myLog':'console.log'
    }