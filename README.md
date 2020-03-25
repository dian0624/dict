技術點:
1. 使用**文本資料讀取**技術讀取字典單字資料，並使用**正則表達式re模塊**匹配所需單詞與解釋，
   並且採用**關聯式數據庫MySQL**，進行英文字典數據的存儲。
2. MySQL數據庫構建3張表，表結構 id 均採用int(11)、**主鍵索引、自增長屬性，內容均設定為非空not null**。
   1. dict 單詞表 : word(varchar(32))、 info(text)
   2. user_all 客戶表 : user(varchar(32))、password(varchar(32))
   3. history 查詢紀錄 : user(varchar(32))、word(varchar(32))、time(timestamp)
3. 服務端與客戶端使用**socket模塊**函式組合，採用傳輸層**tcp流式套接字**進行資料傳輸。
   1. 客戶端利用**sys.argv**綁定用戶啟動程序時命令行參數的列表，利用**try except捕獲與處理錯誤資訊**，輸入密碼時使用**getpass隱形輸入**。
   2. 服務端使用**pymysql**模塊函式調用數據庫資料，作為和客戶端數據互動的基礎，並使用**fork多進程**技術進行多個客戶端於不同進程間的訪問，以及使用
      **signal函式**避免殭屍進程的產生占用系統資源。
--------------------------------------------------------------------------------------------      
功能說明：
1. 用戶可以登錄和註冊
   登錄憑借用戶名密碼即可
   註冊要求用戶必須填寫用戶名和密碼
   用戶名要求不能夠重覆

2. 字典內容與用戶資訊用數據庫長期保存

3. 能夠滿足多個用戶同時登陸操作的需求
![image](https://github.com/dian0624/dict/blob/master/image2/666.jpg) ![image](https://github.com/dian0624/dict/blob/master/image2/777.jpg)
4. 功能分為客戶單和服務端，客戶單主要發起請求，服務端處理請求，用戶啟動客戶端即進入一級界面

     | 登陸 | 註冊 | 退出 |
![image](https://github.com/dian0624/dict/blob/master/image2/444.jpg)
	 
5. 用戶登錄後即進入二級界面

     | 查單詞 | 查看歷史記錄 | 退出 |

     查單詞 ： 輸入單詞，顯示單詞意思，可以循環查詢。輸入 ## 表示退出查詞

     查看歷史記錄： 查看當前用戶的歷史查詞記錄
        name     word    time     
     退出 ： 退出到一級界面
![image](ttps://github.com/dian0624/dict/blob/master/image2/555.jpg)


