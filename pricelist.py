#выгрзка прайс листа в excell

import pyodbc
import pandas as pd
import xlsxwriter
import datetime

conn = pyodbc.connect("Driver={SQL Server Native Client 10.0};"
                        "Server=kassa\\sqlexpress;"
                        "Database=farma;"
                        "uid=user;pwd=password")

query = 'select * from ostatki order by NAME'
df = pd.read_sql_query(query, conn)
filename = str (datetime.date.today())
filename+='.xlsx'
print (filename)


workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()
# name , prod_name , cnt_name , quantity_rem , price_sal , price_sup  , important

xlrow = 0
xlcol = 0
bold = workbook.add_format({'bold': True})
worksheet.write(xlrow, 0, 'Наименование', bold)
worksheet.write(xlrow, 1, 'Производитель',bold)
worksheet.write(xlrow, 2, 'Страна',bold)
worksheet.write(xlrow, 3, 'Количество',bold)
worksheet.write(xlrow, 4, 'Розничаня цена ',bold)
xlrow+=1

for row in df.iterrows() :
    if float (row[1].PRICE_SUP) ==0:
        continue
    isimportant = int (row[1].IMPORTANT)
    worksheet.write(xlrow, 0, str (row[1].NAME))
    worksheet.write(xlrow, 1, str (row[1].prod_name))
    worksheet.write(xlrow, 2, str (row[1].cnt_name))
    worksheet.write(xlrow, 3, str (row[1].QUANTITY_REM))
    if isimportant==1:
        worksheet.write(xlrow, 4, str (round(row[1].PRICE_SAL,2)))
    else:
        worksheet.write(xlrow, 4, str(round(float (row[1].PRICE_SUP*1.5),2)))
    xlrow += 1




