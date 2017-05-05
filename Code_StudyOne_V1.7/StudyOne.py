import csv
import math
import numpy
import random
from numpy import *
import redis_test


#loading库包含了导入csv文件并转化为矩阵的函数
import loading

#输入一个数组numbers_mean并计算其均值
def MeanCalculate(numbers_mean):
    return sum(numbers_mean) / float(len(numbers_mean))



#输入numbers_stdev数组并计算标准差
def StandardDeviation(numbers_stdev):
    #先计算均值
    avg = MeanCalculate(numbers_stdev)
    #均值与每个数的差平方和除以N-1，最后返回开根号
    variance = sum([pow(x - avg, 2) for x in numbers_stdev]) / float(len(numbers_stdev) - 1)
    return math.sqrt(variance)

#得出正态分布函数，根据正态分布函数，输入x值，均值和方差，返回x所在位置的值
def calculateProbability(x, numbers_mean, numbers_stdev):
    exponent = math.exp(-(math.pow(x - numbers_mean, 2) / (2 * math.pow(numbers_stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * numbers_stdev)) * exponent

#计算积分，计算从0到x位置的积分值
def GenerateData(x, mean, stdev):
    datas = []
    n = int(x/0.1)
    r=0
    #从0开始每一步长为0.01计算x的值并最后求和，得出积分值
    for i in range(0,n):
        datas.append(calculateProbability(r, mean, stdev))
        r = r+0.1

    return float(sum(datas))

#计算排名，输入想要查询的考试名，成绩表，考试表
def StudyRanking(TestName,ScoreList,TestList):
    #导入文件并筛选出对应考试的成绩表
    List_Score = loading.loadCsv(ScoreList)
    List_Test = loading.loadCsv(TestList)
    MatScore = []
    #将所有考试名的成绩组成一个矩阵
    for i in range(len(List_Score)):
        #List_Score表格里第二项对应的就是考试名，符合考试名的选出添加至矩阵MatScore
        if(List_Score[i][1] == TestName):
            #MatScore矩阵为每个学生的学号，考试名，该考试每道题分数，该试题的总得分
            MatScore.append(List_Score[i]);
    #从考试表中选出所选考试的每道题的分数值作为列表Test_Each_Value:考试名，每道题的分值，总分值
    Test_Each_Value = List_Test[int(TestName)]
    NumberOfStudent = len(MatScore)


    print(NumberOfStudent)
    print(Test_Each_Value)
    print(MatScore)

# 求出每道题的百分比得分并转置
    #len(MatScore[0]-2)是因为要减去学号和考试名，得出题目和总分的总维数；len(MatScore)为学生数
    Percentage_rotate = zeros([len(MatScore[0]) - 2, len(MatScore)])
    for j in range(len(MatScore)):
        for i in range(len(MatScore[0]) - 2):
            Percentage_rotate[i][j] = MatScore[j][i + 2];
            Percentage_rotate[i][j] = Percentage_rotate[i][j] / float(Test_Each_Value[i + 1]);

# 各题的平均值
    Mean_Each_Question = zeros(len(MatScore[0]) - 2)
    #其中最后一项Mean_Each_Question[-1]为考试总分的平均值
    for i in range(len(MatScore[0]) - 2):
        Mean_Each_Question[i] = MeanCalculate(Percentage_rotate[i])



# 计算每道题以及总分的标准差
    stdev_Score = zeros(len(MatScore[0]) - 2)
    #最后一项算出的是总分标准差
    for i in range(len(MatScore[0]) - 2):
        stdev_Score[i] = StandardDeviation(Percentage_rotate[i])




# 计算每个人每题的‘积分拉分值’（得分积分减去平均积分）
    AreaMean = zeros([len(MatScore[0]) - 2, len(MatScore)])
    AreaEach = zeros([len(MatScore[0]) - 2, len(MatScore)])
    for i in range(len(Percentage_rotate)):
        for j in range(len(Percentage_rotate[0])):
            # AreaMean矩阵为每个人每道题的积分值；
            AreaMean[i][j] = GenerateData(Percentage_rotate[i][j], Mean_Each_Question[i], stdev_Score[i]);
            # AreaEach是每个学生每道题积分值减去对应正态分布的从0到mean的积分值
            AreaEach[i][j] = AreaMean[i][j] - GenerateData(Mean_Each_Question[i], Mean_Each_Question[i], stdev_Score[i]);

# 计算出每个人的每题的拉分值(题目积分拉分值减去总分积分拉分值)
    #len(MatScore[0])-3是题目数量，不包含总分
    Score_Advance = zeros([len(MatScore[0]) - 3, len(MatScore)])
    for i in range(len(MatScore[0]) - 3):
        for j in range(len(MatScore)):
            #AreaEach[-1][j]为j学生的总分
            Score_Advance[i][j] = AreaEach[i][j] - AreaEach[-1][j];

#转置Score_Advance并对每人的题目拉分值进行排序
    Score_Advance_Rotate = zeros([len(MatScore),len(MatScore[0])-3])
    Ranking_Each_Score = zeros([len(MatScore),len(MatScore[0])-3])
    #先转置
    for j in range(len(MatScore)):
        for i in range(len(MatScore[0]) - 3):
            Score_Advance_Rotate[j][i] = Score_Advance[i][j];
        #再用argsort得出排序以及对应的索引值
        Ranking_Each_Score[j] = Score_Advance_Rotate[j].argsort()+1;
    #返回Score_Advance_Rotate为每人每道题的题目拉分情况，越小补习优先度越高；
    #Ranking_Each_Score为每个学生的题目补习优先度排序，最前的最需要补习和提高

        # 每道题拉分值，值越高越拉分，值越低越拖后腿
    print('the Lafen is ')
    print(Score_Advance)
    print('The rank of Your study question number is :')
    # +1是因为索引值是从0到n-1题，需要全部+1编程输出1-n题的排序
    print(Ranking_Each_Score)

    # 将平均分Mean_Each_Question和方差stdev_Score都上传至redis
    redis_test.UpLoadParameter(Mean_Each_Question, stdev_Score,Test_Each_Value,NumberOfStudent)


    return Score_Advance_Rotate,Ranking_Each_Score
