import os
import re

datafile_path = './data/xxx/realtime/2017/3/06/'

#获取指定路径中所有文件相对路径
def GetFolderFile(folderPath):
    '''
    可以直接在方法冒号后打三个点，回车，pycharm会自动补齐其余的说明
    获取指定路径中所有文件相对路径
    :param folderPath:
    :return:
    '''
    filePathes=[]
    for root,dirs,files in os.walk(folderPath):
        # 此处可以用列表推导
        [filePathes.append(folderPath+f) for f in files]
        # for f in files:
        #     filePathes.append(folderPath+f)

    return filePathes


#将文件夹内路径读成一条内容并合并成list返回
def GetFileData(filePathList):
    resultDataList=[]
    regex_c = re.compile('[A-Z]*')
    regex_s = re.compile('[\s]+')
    for singleFile in filePathList:
        with open(singleFile) as txt:
            lst = txt.readlines()
            result = ''.join(lst)
            # 此处没看明白
            # 你是读取每一行的数据匹配是否包含英文字母，若包含则将英文字母替换为空值
            # 将多个空格替换为一个空格
            result =  regex_s.sub(' ',regex_c.sub('',result))
            resultDataList.append(result)

    return resultDataList


filelist = GetFolderFile(datafile_path)
data = GetFileData(filelist)

for line in data:
    print(line)


    