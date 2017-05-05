import redis_test
import StudyOne
import Add_One
import ExportExcel
import xlwt
import datetime


def main():
    #输入考试名'3'，分数表文件'score3.csv',以及试题文件'test1.csv'
    a = input("Enter the testnumber and the file name of score and test e.g input:4,score4.csv,test1.csv\n").split(",")

    #开始计时
    starttime = datetime.datetime.now()

    #获取拉分值和优先度排名，以及一些参数
    Lafen,Ranking = StudyOne.StudyRanking(a[0],a[1],a[2])

    #结束计时
    endtime = datetime.datetime.now()
    #打出运行时间
    interval = (endtime - starttime).seconds
    print('the time is %f' %interval)

    #保存结果到excel
    ExportExcel.ExportExcel(Lafen,'Lafen')
    ExportExcel.ExportExcel(Ranking,'Ranking')

    #添加新的成绩
    addScore = input("Enter the New Score e.g input:3,0,0,3,3,3,0,3,0,3,0,4,4,0,5,7,6,4,2,7,2,4,63 \n").split(",");
    Add_One.AddOne(addScore)

    return Lafen,Ranking

main()