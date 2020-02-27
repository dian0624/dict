from pymysql import *
import re

f = open('./dict.txt')
db = connect(host = 'localhost',
			user = 'root',
			password = 'a123456',
			database = 'dict_hw')
cur = db.cursor()


for line in f:
	l = re.split(r'\s+',line)
	word = l[0] 
	info = ' '.join(l[1:])

	try:
		cur.execute("insert into dict(word, info) values \
				   ('{}','{}')".format(word,info))
		db.commit()
	except:
		db.rollback()

cur.close()
db.close()
f.close()

