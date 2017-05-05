import redis_test
import StudyOne
from numpy import *

def AddOne(OneScore):
    ParaMean, ParaStdev, Test_Each_Value, NumberOfStudent = redis_test.GetPara()
    if int(NumberOfStudent) > 5:




        for i in range(len(OneScore)):
            OneScore[i] = float(OneScore[i])/float(Test_Each_Value[i+1]);

        AreaNew = zeros([len(OneScore)])
        for i in range(len(OneScore)):
            AreaNew[i] = StudyOne.GenerateData(OneScore[i], ParaMean[i], ParaStdev[i])-StudyOne.GenerateData(ParaMean[i], ParaMean[i], ParaStdev[i]) ;

        Score_Advance = zeros([len(OneScore)-1])
        for i in range(len(OneScore)-1):
            Score_Advance[i] = AreaNew[i] - AreaNew[-1];

        print(Score_Advance)

        Ranking_Each_Score = zeros([len(OneScore)-1])
        Ranking_Each_Score = Score_Advance.argsort() + 1;

        print(Ranking_Each_Score)
