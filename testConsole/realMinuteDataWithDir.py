import os
import re

datafile_path = './data/xxx/realtime/2017/3/06/'

#获取指定路径中所有文件相对路径
def GetFolderFile(folderPath):
    filePathes=[]
    for root,dirs,files in os.walk(folderPath):
        for f in files:
            filePathes.append(folderPath+f)

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
            result =  regex_s.sub(' ',regex_c.sub('',result))
            resultDataList.append(result)

    return resultDataList


filelist = GetFolderFile(datafile_path)
data = GetFileData(filelist)

for line in data:
    print(line)


    