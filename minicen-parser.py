import requests
import pprint
#from bs4 import BeautifulSoup
import pandas as pd
import time
#from yaml import load



#https://api.minicen.ru/cmd/exec?proc=TradePointGet
#список точек у миницен по всем городам

#https://api.minicen.ru/search/main?idTradePoint=13964&Request=&SearchType=2&ReturnType=&Sorting=3&idGroup=1&Page=2&PerPage=0&idAdvDiscountPage=&LongSessionID=
#лек средства по аптеке


#https://api.minicen.ru/search/main?idTradePoint=13964&Request=&SearchType=2&ReturnType=&Sorting=3&idGroup=2&Page=2&PerPage=0&idAdvDiscountPage=&LongSessionID=
#БАДы


## список торговых точек в Петропавловске
#pp.pprint(TradePoints)


urlTradePoints = "https://api.minicen.ru/cmd/exec?proc=TradePointGet"
r = requests.get(urlTradePoints)
data = r.json()
data = data["Data"]
data = data[0]

#pp.pprint(data)
TradePoints = []
for record in data:
    adr = str( record["AddressDostFull"])
    if "Петропавловск" in adr:
        print (record["idRecord"], record["AddressDostFull"])
        TP = {"id":record["idRecord"], "address":record["AddressDostFull"]}
        TradePoints.append(TP)



pp = pprint.PrettyPrinter(indent=4)


params = {
'idTradePoint':14156,
'Request':'',
'SearchType':2,
'ReturnType':'',
'Sorting':3,
'idGroup':1,
'Page=':2,
'PerPage':0,
'idAdvDiscountPage':'',
'LongSessionID':''
}

urlGoods = "https://api.minicen.ru/search/main"
r = requests.get(urlGoods, params=params)
data = r.json()
#pp.pprint(data)
pagination = data['Data'][ 'tovarPagination']
#pp.pprint(pagination)
maxpage = pagination['PageCount']

tovar = []
#exit(0)
for page in range (2,maxpage):
#for page in range (2,25):

    print("Страница ", page, " из ", maxpage)
    time.sleep(5)
    params = {
        'idTradePoint': 14156,
        'Request': '',
        'SearchType': 2,
        'ReturnType': '',
        'Sorting': 3,
        'idGroup': 1,
        'Page': page,
        'PerPage': 0,
        'idAdvDiscountPage': '',
        'LongSessionID': ''
    }
    r = requests.get(urlGoods, params=params)
    data = r.json()
    GroupName = data['Data']['breadcrumbs'][0]['GroupName']
    GoodsList = data['Data']['tovar']

    for Good in GoodsList:
        #print(Good['TovarName'])
        record = {
            'idRecord': Good['idRecord'],
            'TovarName':Good['TovarName'],
            'NameCountry': Good['NameCountry'],
            'NameMaker': Good['NameMaker'],
            'IndzPrice': Good['IndzPrice'],
            'IndzPriceWoDiscount': Good['IndzPriceWoDiscount'],
            'IsFavoriteTovar':Good['IsFavoriteTovar'],
            'Price': Good['Price'],
            'PriceWoDiscount': Good['PriceWoDiscount'],
            'GroupName': GroupName

        }
        tovar.append(record)

#pp.pprint(tovar)

dt = pd.DataFrame(tovar)
#print(dt)
columns = dt.columns.tolist()
columns = columns[::-1]
dt = dt[columns]

dt.to_excel("tovar.xlsx")


exit(0)



