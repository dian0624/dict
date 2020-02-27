＃電子辭典項目_代碼思路
功能說明：
1. 用戶可以登錄和註冊
   登錄憑借用戶名密碼即可
   註冊要求用戶必須填寫用戶名和密碼
   用戶名要求不能夠重覆

2. 使用數據庫長期保存

3. 能夠滿足多個用戶同時登陸操作的需求

4. 功能分為客戶單和服務端，客戶單主要發起請求，服務端處理請求，用戶啟動客戶端即進入一級界面
     登陸   註冊   退出
	 
5. 用戶登錄後即進入二級界面
     查單詞   查看歷史記錄   退出

     查單詞 ： 輸入單詞，顯示單詞意思，可以循環查詢。輸入 ## 表示退出查詞

     查看歷史記錄： 查看當前用戶的歷史查詞記錄
        name     word    time
      
     退出 ： 退出到一級界面
-------------------------------------------------- -----------------------------------