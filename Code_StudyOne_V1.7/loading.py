
import csv
from numpy import *

#输入文件名并导出数据作为矩阵
def loadCsv(filename):
    lines = csv.reader(open(filename, "r"))
    print(lines)
    DataSet = list(lines)
    for i in range(len(DataSet)):
        DataSet[i] = [x for x in DataSet[i]]
    return DataSet




