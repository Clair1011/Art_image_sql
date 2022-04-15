from bs4 import BeautifulSoup
import requests

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

                # art_name = work_object.find('h1').text # 作品名稱

                img = work_object.find('a')
                imgs = img.get(a['href'])
                #print(imgs)

                with open('C:/Users/winni/Desktop/project/img/t','wb') as f:
                #     #將圖片下載下來
                    f.write(imgs.content)

