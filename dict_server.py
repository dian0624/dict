from socket import *
from pymysql import *
import os,sys
import signal
import time

'''
name:   Dian
email:  a5051563@gmail.com
data :  2019-12-24
introduce: mysql server
env: python3.5
'''

# server address
ADDR = ('0.0.0.0', 8888)
# dict.txt
DICT_TXT = './dict.txt'

# 登錄
def login(c,db,data):
	print('登錄操作')
	l = data.split(' ')
	# 帳戶密碼
	name = l[1]
	password = l[2]

	#數據庫連接 查詢
	cur = db.cursor()
	# sql命令，確認用戶及密碼
	sql = "select * from user_all \
	where user='{}' and \
	password=md5('{}')".format(name,password)
	cur.execute(sql)
	#返回單個紀錄，沒有則返回None
	r = cur.fetchone()

	# 返回確認結果
	if r == None:
		c.send(b'fall')
	else:
		print('******%s 登錄成功******'%name)
		c.send(b'ok')


#註冊
def re(c,db,data):
	print('註冊操作')
	while True:
		l = data.split(' ')
		#客戶端註冊姓名
		name = l[1]
		print(name,'申請註冊')

		# 查找數據庫，姓名能否使用
		cur = db.cursor()
		# sql，確認用戶名是否存在
		sql = "select * from user_all\
		where user='%s'"%(name)

		cur.execute(sql)
		r = cur.fetchone()

		if r == None:
			print('************')
			# 存在發送ok,並接收客戶端發送之密碼，並寫入數據庫
			c.send(b'ok')
			#接收密碼
			password = c.recv(1024).decode()
			if password == 'error':
				break

			#sql 寫入密碼
			sql = "insert into user_all(user,password)\
			 value('{}',md5('{}'))".format(name,password)

			try:
				cur.execute(sql)
				db.commit()
				# 發送訊息給客戶端 註冊成功
				c.send('註冊成功'.encode())
				print("%s 註冊成功"%name)
				print('************')
				break
			except Exception as e:
				db.rollback()
				print(e)
				c.send('註冊失敗，請重新註冊'.encode())

		else:
			# 存在的話發送existe
			c.send(b'existe')
			break

#查詢
def sel(c,db,data):
	while True:
		#客戶端 單詞
		l = data.split(' ')
		name = l[1]
		word = l[2]
		#查找數據庫
		cur = db.cursor()
		sql = "select info from dict\
		where word='%s'"%(word)
		cur.execute(sql)
		r = cur.fetchone()

		#單詞存在，傳回ok +單詞解釋
		if r == None:
			c.send('沒有這個單詞，請重新輸入！'.encode())
			break
		else:
			print('{} 查詢 {}'.format(name,word))
			c.send('ok**{}'.format(r[0]).encode())

			# 將搜尋結果寫入歷史紀錄數據表 名字 單詞 時間
			sql = "insert into history(user,word,time)\
			 values('%s','%s',now())"%(name,word)
			cur.execute(sql)
			print('一條歷史紀錄寫入')
			print('********************')
			db.commit()
			break

#歷史紀錄
def his(c,db,data):
	l = data.split(' ')
	name = l[1]
	print('%s 查看歷史紀錄'%name)
	#查找數據庫
	sql = "select * from history \
	where user='%s'\
	order by time desc limit 10"%(name)
		
	cur = db.cursor()
	cur.execute(sql)

	r = cur.fetchall()
	if r == None:
		c.send(b'fall')
		return
	else:
		c.send(b'ok')

	for i in r:
		#防止沾粘
		time.sleep(0.1)
		msg = "{} | {} | {}".format(i[1],i[2],i[3:][0])
		c.send('{}'.format(msg).encode())
	#防止ftp傳送沾粘
	time.sleep(0.2)
	c.send(b'##')


def main():
	# 數據庫連接
	db = connect(host = 'localhost',
				user = 'root',
				password = 'a123456',
				database = 'dict_hw')

	# 創建套接字 ftp
	s = socket()
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.bind(ADDR)
	s.listen(5)

	#忽略子進程狀態改變,子進程退出自動由系統處理
	signal.signal(signal.SIGCHLD,signal.SIG_IGN) 

	while True:
		try:
			c, addr = s.accept()
		except KeyboardInterrupt:
			s.close()
			sys.exit('服務器退出')
		except Exception as e:
			print('Error:',e)
			continue

		print('已連結客戶端：',addr)

		#創建立子進程
		pid = os.fork()
		if pid == 0:
			s.close()

			# 判斷客戶端請求
			while True:
				data = c.recv(1024).decode()
				if not data or data[0] == 'E':
					c.close()
					sys.exit('客戶端退出')
				# 登錄
				elif data[0] == 'L':
					login(c,db,data)
				# 註冊
				elif data[0] == 'R':
					re(c,db,data)
				#查詢
				elif data[0] == 'S':
					sel(c,db,data)
				#查看歷史紀錄
				elif data[0] == 'H':
					his(c,db,data)
		else:
			c.close()
			continue


if __name__ == '__main__':
	main()