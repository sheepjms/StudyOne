import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def UpLoadParameter(mean,stdev,Test_Each_Value,NumberOfStudent):

    r['ParaMean'] = 'ParaMean'
    r.set('ParaMean', mean)
    r['ParaStdev'] = 'ParaStdev'
    r.set('ParaStdev', stdev)
    r['ParaTest'] = 'ParaTest'
    r.set('ParaTest', Test_Each_Value)
    r['ParaNumber'] = 'ParaNumber'
    r.set('ParaNumber', NumberOfStudent)

def GetPara():
    para1 = r.get('ParaMean')
    para2 = r.get('ParaStdev')
    para3 = r.get('ParaTest')
    para4 = r.get('ParaNumber')
    return para1,para2,para3,para4

