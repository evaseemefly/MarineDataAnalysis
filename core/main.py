
import os
import bin.MarineData
# 当前项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class OperEnvironment:
    def __init__(self,factory):
        '''
        传入一个工厂
        :param factory:
        '''
        self.marineData=factory
        pass

    def run(self):
        self.marineData.readData(BASE_DIR+r'/data/XXX/perclock/2017/11/29/at1129.07422')
        pass

def main():
    '''
    主函数
    :return:
    '''
    # 1、根据配置文件或输入选择当前是读取整点还是分钟的数据
    #
    print(BASE_DIR)
    en=bin.MarineData.PerclockData('123','123')
    environment=OperEnvironment(en)
    environment.run()
    pass

if __name__=='__main__':
    main()

