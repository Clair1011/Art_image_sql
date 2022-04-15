import mysql.connector
import base64
import io
import PIL.Image

line_split = "------------------------------------------------"
line_new = "\n"

# 設定資料庫連線資訊
mydb = mysql.connector.connect(
        # host="127.0.0.1",port=3307, # mysql 的主機ip
        host="127.0.0.1",port=3306, # mysql 的主機ip
        user="root",	  # mysql 的 username
        password="",	  # mysql 的password
        database="arts",   # 要查詢的資料庫名稱
        charset="utf8"    # 資料庫編碼
    )

def getKeyWords(sql, col_name):
    mycursor = mydb.cursor()
    
    key = str(col_name).strip()
    
    if sql:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        
        total = mycursor.rowcount
        
        if total > 0:
            #change SQL result to dictionary
            columns = [column[0] for column in mycursor.description]
            results = []
            for row in myresult:
                results.append(dict(zip(columns, row)))

            print(line_new)
            print(line_split)
            print("關連字數: {}".format(total))
            print(line_new)
            row = 1
            for result in results:
                print("{}. - {}".format(row,result[key]))
                row = row + 1

            print(line_split)
            
# 查詢資料庫的函數
def selectData(fun, value):
    mycursor = mydb.cursor()
    sql1 = ""
    if fun == 1:   # 輸入 1 依據作者資訊做模糊查詢
        mycursor.execute("SELECT * FROM artdata where author like '%"+value+"%'")
        sql1 = "SELECT DISTINCT author FROM artdata WHERE author like '%"+value+"%'"
        col_name = "author"
        myresult = mycursor.fetchall()
    elif fun == 2: # 輸入 2 依據作品名稱做模糊查詢
        mycursor.execute("SELECT * FROM artdata where art_name like '%"+value+"%'")
        sql1 = "SELECT DISTINCT art_name FROM artdata WHERE art_name like '%"+value+"%'"
        col_name = "art_name"
        myresult = mycursor.fetchall()
    elif fun == 3: # 輸入 3 依據作品材質做模糊查詢
        mycursor.execute("SELECT * FROM artdata where material like '%"+value+"%'")
        sql1 = "SELECT DISTINCT material FROM artdata WHERE material like '%"+value+"%'"
        col_name = "material"
        myresult = mycursor.fetchall()
    
    # for x in myresult: # 將查詢到的資訊輸入到 console
        # print("編號:",x[2], "作品名稱:",x[1], "作者:", x[3], "年份:", x[4], "尺寸:", x[5], "材質:", x[6])
    
    total = mycursor.rowcount 
    
    if total > 1:
        #change SQL result to dictionary
        columns = [column[0] for column in mycursor.description]
        results = []
        for row in myresult:
            results.append(dict(zip(columns, row)))

        for result in results:
            printArtData(result)
                   
        print(line_new)
        print(line_split)
        print("查詢結果:    {}".format(total))
        print(line_new)
        print("輸入 1 - 取得關連字")
        print("輸入 0 - 返回")
        print(line_new)
        print(line_split)
        
        while True:   
                    
            user_input = input("\n請輸入:") # 接收使用者需要進入的功能
            if user_input == '1':    
                getKeyWords(sql1, col_name) 
                break
            elif user_input == '0':  
                break
            else: # 輸入錯誤，從迴圈從頭再開始
                check_user_input(user_input)
        
        
    else:
        
        print("沒有結果\n")

def getSimilarNumber(number):
    if number:        
        temp = str(number).strip()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM artdata where number like '%"+temp+"%'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        
        total = mycursor.rowcount 
        
        if total > 1:
            #change SQL result to dictionary
            columns = [column[0] for column in mycursor.description]
            results = []
            for row in myresult:
                results.append(dict(zip(columns, row)))
            
            for result in results:
                db_art_name = str(result["art_name"]).strip()
                db_number = str(result["number"]).strip()
                print(line_split)
                print("作品名稱:    {}\n編號:   {}".format(db_art_name,db_number))
                
            print("\n查詢結果:    {}\n".format(total))
            print(line_split)
            print("請輸入正確編號以取得圖片:")
            data = input() # Input number
            getSimilarNumber(data)
            
        else:
            columns = [column[0] for column in mycursor.description]
            results = []
            for row in myresult:
                results.append(dict(zip(columns, row)))
            
            for result in results:
                if result['image']:
                    db_image=base64.b64decode(result['image'])
                    file_like=io.BytesIO(db_image)
                    img=PIL.Image.open(file_like)
                    img.show()
                
                printArtData(result)
        
     

def printArtData(result):
    if result:        
        art_name = str(result["art_name"]).strip()
        number = str(result["number"]).strip()
        author = str(result["author"]).strip()
        year = str(result["year"]).strip()
        size = str(result["size"]).strip()
        material = str(result["material"]).strip()
         
        print(line_split)
        print("作品名稱:    {}".format(art_name))
        print("編號:   {}".format(number))
        print("作者:   {}".format(author))
        print("年份:   {}".format(year))
        print("尺寸:   {}".format(size))
        print("材質:   {}".format(material))

def check_user_input(data):
    try:
        # Convert it into integer
        val = int(data)
    except ValueError:
        print("輸入錯誤。 (輸入 : {})".format(data))

#Main
while True:
    print(line_new)    
    print("===== 歡迎來到世界名畫資料庫 =====")
    print(line_new)
    print("功能介紹")
    print("輸入1 - 依作者名稱查詢(模糊查詢)")
    print("輸入2 - 依作品名稱查詢(模糊查詢)")
    print("輸入3 - 依作品材質查詢(模糊查詢)")
    print("輸入4 - 查詢編號取得圖片")
    print("輸入9 - 退出")
    print(line_new)
    print("==================================")    
    
    user_input = input("\n請輸入:") # 接收使用者需要進入的功能
    if user_input == '1':    
        data = input("請輸入作者名稱:") # 輸入作者名稱
        selectData(1, data) # 依據使用者輸入的作者資訊丟到 selectData 函數查詢結果 
    elif user_input == '2':  
        data = input("請輸入作品名稱:") # 輸入作品名稱
        selectData(2, data) # 依據使用者輸入的作品資訊丟到 selectData 函數查詢結果 
    elif user_input == '3':  
        data = input("請輸入作品材質:") # 輸入作品材質
        selectData(3, data) # 依據使用者輸入的材質資訊丟到 selectData 函數查詢結果
    elif user_input == '4':  
        data = input("請輸入查詢編號:") # Input number
        getSimilarNumber(data) 
    elif user_input == '9': # 離開查詢功能介面
        print("bye! bye!")
        break
    else: # 輸入錯誤，從迴圈從頭再開始
        check_user_input(user_input)