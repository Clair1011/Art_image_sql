#!pip3 install beautifulsoup4 
#!pip3 install mysql-connector-python 
#!pip3 install requests 

from bs4 import BeautifulSoup
import requests
import mysql.connector # mysql 資料庫模組

# 資料設定資訊 mysql
mydb = mysql.connector.connect(
        host="127.0.0.1",port=3307, 
        user="root",    
        password="",    
        database="art", 
        charset="utf8" 
    )

# 新增資料到資料庫的函數
def insertData(count, art_name, number, author, year, size, material, visit):
    mycursor = mydb.cursor()
    # 新增資料的指令
    sql = "INSERT INTO `artdata` (`num`, `art_name`, `number`, `author`, `year`, `size`, `material`, `visit`) VALUES ('"+str(count)+"','"+art_name+"','"+number+"','"+author+"','"+year+"','"+size+"','"+material+"','"+visit+"')"
    # 把資料新增到資料庫的 artdata table 中
    mycursor.execute(sql)
    mydb.commit()

html_data = requests.get("https://www.ss.net.tw/") # 要爬的網址的首頁

soup = BeautifulSoup(html_data.text, 'html.parser') # 把首頁的爬到的 html code 丟到物件中
count = 1
for a in soup.find_all('a', class_="list-group-item"): # 尋找目前的所有畫家
    if '全部' not in a['title']: # 因為全部下面已有各別子分類，為了不要重複爬蟲 所以母分類不爬 因為已經有子分類了 只能爬子分類就可以爬到全部了
        
        href = a['href'] # 取得畫家作品的連結
        title =  a['title'] # 取得畫家名稱

        # 取得畫家頁面後開始爬他的作品列表

        second_data = requests.get(href)
        second_object = BeautifulSoup(second_data.text, 'html.parser') # 把畫家作品列表爬到的 html code 丟到物件中

        datas = second_object.find_all('div', class_="card") # 爬到此畫家的作品

        for data in datas: # 爬每個作品詳細資料頁的內容
            for t in data.find_all('a'):
                print("Found the URL:", t['href']) 

                # 第三層取得作品的詳細資料
                work_data = requests.get(t['href'])
                work_object = BeautifulSoup(work_data.text, 'html.parser') # 把作品詳細資料內容爬到的 html code 丟到物件中
               
                work_object = work_object.find('div', id="productsInfo")
                
                art_name = work_object.find('h1').text # 作品名稱
              
                number='' # 編號
                author='' # 作者
                year='' # 年份
                size='' # 尺寸
                material='' # 材質
                visit=''    # 瀏覽人數
                for li in work_object.find_all('li'): # 取得 li 中的資料 分別為 編號、作者、年份、尺寸、材質、瀏覽人數
                    label = li.find('label')
                   
                    if '編　　號' in label.text:
                        number = li.text.replace(label.text, "")
                    elif label.text == '作　　者':
                        author = li.text.replace(label.text, "")
                    elif label.text == '年　　份':
                        year = li.text.replace(label.text, "")
                    elif label.text == '原作尺寸':
                        size = li.text.replace(label.text, "")
                    elif label.text == '原作材質':
                        material = li.text.replace(label.text, "")
                    elif label.text.replace(" ", "") == '瀏覽人次':
                        visit = li.text.replace(label.text, "")



                                        
                insertData(count, art_name,number,author,year,size,material,visit)
                count = count + 1