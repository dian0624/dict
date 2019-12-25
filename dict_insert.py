from pymysql import *
import re

f = open('./dict.txt')

#數據庫連接
db = connect(host = 'localhost',
			user = 'root',
			password = 'a123456',
			database = 'dict_hw')

cur = db.cursor()

# 文檔讀取
for line in f:
	# 拆分數據字段 [單字，解析],用正則表達式輔助拆分
	l = re.split(r'\s+',line)
	# 單字
	word = l[0]
	# 解析 
	info = ' '.join(l[1:])
	# print(word,info)


	# 寫入數據庫
	try:
		cur.execute("insert into dict(word, info) values \
				   ('{}','{}')".format(word,info))
		db.commit()
	except:
		#捕獲錯誤數據會遺失一些
		db.rollback()

cur.close()
db.close()
f.close()





	
	