from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests
import mysql.connector
import time
import sys
import os




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset='utf8',  
  database="gold"
)

def xnowtime():
    dt = datetime.now()
    sdt = str(dt)
    return sdt[0:19]


def insdata(data):
    dt = datetime.now()
    sdt = str(dt)

    mycursor = mydb.cursor()
    sql = "INSERT INTO `tb_gold` (`golddate`, `nqy`, `blsell`, `blbuy`, `omsell`, `ombuy`, `cdate`) VALUES (%s,%s, %s,%s,%s,%s,%s)"
    val = (
             data['asdate'],
             data['nqy'],
             data['blsell'],
             data['blbuy'],
             data['omsell'],
             data['ombuy'],
             sdt[0:19]
           )


    print(sql,val )
    mycursor.execute(sql, val)

    mydb.commit()
    print("insert complated..!!")
    mycursor.close()
    

def seldata():
    mycursor = mydb.cursor()
    sql = "select * from tb_gold  order by id desc limit 1 ;"

    mycursor.execute(sql)

    myresult = mycursor.fetchone()
    mycursor.close()


    return(myresult)

def selectdata(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    mycursor.close()
    return(myresult)


url = 'https://www.goldtraders.or.th/'

res = requests.get(url)
res.encoding = "utf-8"


soup = BeautifulSoup(res.text, 'html.parser') #'lxml'
time.sleep(0.5)

retime= []

for el in soup.findAll('span', attrs={'id': 'DetailPlace_uc_goldprices1_lblAsTime'}):
    
    astime = ''.join(el.findAll(text=True))
    retime  = astime.split(" ")
    
    asdate = retime[0] + ' ' + retime[2]
    nqy = retime[5].replace(")","")

for el in soup.findAll('span', attrs={'id': 'DetailPlace_uc_goldprices1_lblBLSell'}):    
    BLSell = ''.join(el.findAll(text=True))
    #print(BLSell)
    blsell = BLSell
   

for el in soup.findAll('span', attrs={'id': 'DetailPlace_uc_goldprices1_lblBLBuy'}):    
    BLBuy = ''.join(el.findAll(text=True))
    #print(BLBuy)
    blbuy = BLBuy
    

for el in soup.findAll('span', attrs={'id': 'DetailPlace_uc_goldprices1_lblOMSell'}):    
    OMSell = ''.join(el.findAll(text=True))
    #print(OMSell)
    omsell = OMSell
  

for el in soup.findAll('span', attrs={'id': 'DetailPlace_uc_goldprices1_lblOMBuy'}):    
    OMBuy = ''.join(el.findAll(text=True))
    #print(OMBuy)
    ombuy = OMBuy
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '/getgold.json')    
ar_data =  {
             'asdate':asdate,
             'nqy':nqy,
             'blsell':blsell,
             'blbuy':blbuy,
             'omsell':omsell,
             'ombuy':ombuy    ,
             'pathjson':file_path
           }

print(file_path)
with open("getgold.json", "w") as outfile:
    json.dump(ar_data, outfile)
#print('ar_data:',ar_data)
#print(seldata())
if(seldata() == None ):
 print('non data')
 insdata(ar_data)

else:
   zdata =  seldata()
   print(zdata[1])
   if zdata[1] == asdate :
       print('not update')
   else:
       insdata(ar_data)
       print('update')
       
 



   









    
       
       

