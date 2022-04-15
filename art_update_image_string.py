
from bs4 import BeautifulSoup
import requests
import mysql.connector # mysql 資料庫模組
import base64
import os
import time

# 資料設定資訊 mysql
mydb = mysql.connector.connect(
        host="127.0.0.1",port=3307, 
        #host="127.0.0.1",port=3306, 
        user="root",    
        password="",    
        database="arts", 
        charset="utf8" 
    )

# 新增資料到資料庫的函數
# def insertData(count, art_name, number, author, year, size, material, visit):
    # mycursor = mydb.cursor()
    # # 新增資料的指令
    # sql = "INSERT INTO `artdata` (`num`, `art_name`, `number`, `author`, `year`, `size`, `material`, `visit`) VALUES ('"+str(count)+"','"+art_name+"','"+number+"','"+author+"','"+year+"','"+size+"','"+material+"','"+visit+"')"
    # # 把資料新增到資料庫的 artdata table 中
    # mycursor.execute(sql)
    # mydb.commit()

def updateImage(art_numbers):
    cursor = mydb.cursor()
    
    for art_number in art_numbers:
        num = str(art_number['num']).strip()
        number = str(art_number['number']).strip()
        
        # img_link 
        img_link = "https://www.ss.net.tw/images/product_images/popup_images/"+number+".jpg"
        img = requests.get(img_link)  # dl img
        encodestring = base64.b64encode(img.content)
        sql = "UPDATE artdata SET image=%s WHERE num="+num
        cursor.execute(sql,(encodestring,))
        mydb.commit() 
        print("Done :"+num)
        
    #mydb.commit()

def getAllName():
    cursor = mydb.cursor()
    # 新增資料的指令
    sql = "SELECT num, number FROM artdata"
    # 把資料新增到資料庫的 artdata table 中
    cursor.execute(sql)
    
    columns = [column[0] for column in cursor.description]
    print(columns)
    
    results = []
    i=0
    for row in cursor.fetchall():
        # Testing only
        # i = i+1
        # if i > 10:
            # break
        results.append(dict(zip(columns, row)))
        
    # print(results)
    return results
    
    
    # result_set = mycursor.fetchall()
    # for row in result_set:
        # print(row)
    
    # mydb.commit()    
    
art_numbers = getAllName()
updateImage(art_numbers)
# print(art_numbers)

# for art_number in art_numbers:
    # print('-------------------')
    # print(art_number['num'])
    # print(art_number['number'])


