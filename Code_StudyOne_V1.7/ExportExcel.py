

import xlwt
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1',cell_overwrite_ok=True)

#这样表单就被创建了,写入数据也很简单：
# indexing is zero based, row then column
def ExportExcel(exportData,exportName):
    for i in range(len(exportData)):
        for j in range(len(exportData[0])):
            sheet.write(i,j,exportData[i][j]);
    # 之后，就可以保存文件(这里不需要想打开文件一样需要close文件)：

    wbk.save('%s.xls' %exportName )

