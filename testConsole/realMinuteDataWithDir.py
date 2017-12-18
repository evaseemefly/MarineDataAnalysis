import numpy as np
import pandas as pd
import os
import re
from io import StringIO
datafile_path = '../data/xxx/realtime/2017/11/01/'

table_index='DT,WT,SL,WL,DT1,AT,BP,HU,RN,WS1,WS2,WS3,WS4,WS5,WS6,WS7,WS8,WS9,WS10'.split(',')

#获取指定路径中所有文件相对路径
def GetFolderFile(folderPath):
    '''
    可以直接在方法冒号后打三个点，回车，pycharm会自动补齐其余的说明
    获取指定路径中所有文件相对路径
    :param folderPath:
    :return:
    '''
    file_pathes=[]
    for root, dirs, files in os.walk(datafile_path, topdown=False):
        if(len(files)!=0):
            for name in files:
                file_pathes.append(root+'/'+name)

    return file_pathes


#将文件夹内路径读成一条内容并合并成list返回
def GetFileData(filePathList):
    '''
    读取txt文件并转换为dataframe，暂时先转换成lst，还没想好怎么合并，指定好列了应该好合并
    '''
    lst,errlst=[],[]
    reg_removeHead = re.compile('[A-Z]*?[\s]+')
    reg_removeEnter = re.compile('\n')
    for singleFile in filePathList:
        try:
            with open(singleFile) as txt:
                result = txt.read()
                result = reg_removeEnter.sub('', result) #移除换行
                result = reg_removeHead.sub(' ', result) #移除标题等待重新指定
                result = result.lstrip(' ')
                tempdf=pd.read_csv(StringIO(result),delimiter='\s',header=None,names=table_index,engine='python')
                tempdf.columns=table_index
                lst.append(tempdf)
        except Exception as err:
#             print(singleFile) #为什么这有个try catch 这个数据不但格式不太好，而且编码还不一样，有些是unicode 有些是gbk 莫名其妙，而且是偶尔有
#             print(err)
            errlst.append(err)
    return (lst,errlst)

                      
def GetRealTimeDataFrame(filePathList):
    dflst,errlst = GetFileData(filePathList)
    print('获取数据',len(dflst),'行,因错误失去数据',len(errlst))
    if(len(dflst)>1):
        temp = dflst[0]
        for i in range(1,len(dflst)):
            temp = temp.append(dflst[i],ignore_index=True)
        return (temp,errlst)
    else:
        return (dflst,errlst)


#'这下边是测试'
df,err = GetRealTimeDataFrame(GetFolderFile(datafile_path))
df.head()
