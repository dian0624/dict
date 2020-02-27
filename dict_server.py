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

ADDR = ('0.0.0.0', 8888)
DICT_TXT = './dict.txt'

def login(c,db,data):
	print('登錄操作')
	l = data.split(' ')
	name = l[1]
	password = l[2]

	cur = db.cursor()
	sql = "select * from user_all \
	where user='{}' and \
	password=md5('{}')".format(name,password)
	cur.execute(sql)
	r = cur.fetchone()

	if r == None:
		c.send(b'fall')
	else:
		print('******%s 登錄成功******'%name)
		c.send(b'ok')


def re(c,db,data):
	print('註冊操作')
	while True:
		l = data.split(' ')
		name = l[1]
		print(name,'申請註冊')

		cur = db.cursor()
		sql = "select * from user_all\
		where user='%s'"%(name)

		cur.execute(sql)
		r = cur.fetchone()

		if r == None:
			print('************')
			c.send(b'ok')
			password = c.recv(1024).decode()
			if password == 'error':
				break
			sql = "insert into user_all(user,password)\
			 value('{}',md5('{}'))".format(name,password)

			try:
				cur.execute(sql)
				db.commit()
				c.send('註冊成功'.encode())
				print("%s 註冊成功"%name)
				print('************')
				break
			except Exception as e:
				db.rollback()
				print(e)
				c.send('註冊失敗，請重新註冊'.encode())
		else:
			c.send(b'existe')
			break


def sel(c,db,data):
	while True:
		l = data.split(' ')
		name = l[1]
		word = l[2]
		cur = db.cursor()
		sql = "select info from dict\
		where word='%s'"%(word)
		cur.execute(sql)
		r = cur.fetchone()

		if r == None:
			c.send('沒有這個單詞，請重新輸入！'.encode())
			break
		else:
			print('{} 查詢 {}'.format(name,word))
			c.send('ok**{}'.format(r[0]).encode())
			sql = "insert into history(user,word,time)\
			 values('%s','%s',now())"%(name,word)
			cur.execute(sql)
			print('一條歷史紀錄寫入')
			print('********************')
			db.commit()
			break


def his(c,db,data):
	l = data.split(' ')
	name = l[1]
	print('%s 查看歷史紀錄'%name)
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
		time.sleep(0.1)
		msg = "{} | {} | {}".format(i[1],i[2],i[3:][0])
		c.send('{}'.format(msg).encode())
	time.sleep(0.2)
	c.send(b'##')


def main():
	db = connect(host = 'localhost',
				user = 'root',
				password = 'a123456',
				database = 'dict_hw')

	s = socket()
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.bind(ADDR)
	s.listen(5)
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

		pid = os.fork()
		if pid == 0:
			s.close()
			while True:
				data = c.recv(1024).decode()
				if not data or data[0] == 'E':
					c.close()
					sys.exit('客戶端退出')
				elif data[0] == 'L':
					login(c,db,data)
				elif data[0] == 'R':
					re(c,db,data)
				elif data[0] == 'S':
					sel(c,db,data)
				elif data[0] == 'H':
					his(c,db,data)
		else:
			c.close()
			continue


if __name__ == '__main__':
	main()