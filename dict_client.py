from socket import *
import os,sys
import getpass

def menu_1():
	print(" ----------- ")
	print("| "+" 一級界面 "+"|")
	print(" ----------- ")
	print("| "+"1. 註冊  "+" |")
	print("| "+"2. 登錄  "+" |")
	print("| "+"3. 退出  "+" |")
	print(" ----------- ")


def login(s):
	name = input('請輸入用戶名：')
	password = getpass.getpass()
	msg = 'L {} {}'.format(name, password)
	s.send(msg.encode())
	data = s.recv(1024).decode()

	if data == 'ok':
		print('登錄成功')
		return name
	else:
		print('用戶或密碼錯誤')
		return False


def re(s):
	while  True:
		name = input('請輸入用戶註冊名：')
		if (' ' in name):
			print('用戶名不能加空格')
			continue
		if not name :
			print('請輸入正確格式')
			break
		s.send('R {}'.format(name).encode())
		data = s.recv(1024).decode()
		if data == 'ok':
			password = getpass.getpass('請輸入密碼：')
			if not password:
				break
			password1 = getpass.getpass('請在輸入一次密碼：')
			if password != password1:
				print('兩次密碼不同,註冊失敗')
				s.send(b'error')
				break

			s.send(password.encode())
			msg = s.recv(1024).decode()
			print(msg)
			break
		else:
			print('此用戶已存在')
			continue


def client_exit(s):
	s.send(b'E')
	s.close()
	sys.exit('謝謝使用')


def login_2(s,name):
	while True:
		print(" -------------- ")
		print("| "+" 二級界面   "+" |")
		print(" -------------- ")
		print("| "+"1. 查詢     "+" |")
		print("| "+"2. 歷史紀錄 "+" |")
		print("| "+"3. 退出     "+" |")
		print(" -------------- ")
		
		try:
			msg = input('請選擇功能：')
		except Exception as e:
			print('請輸入正確功能！') 
			continue

		if msg not in ['1','2','3'] :
			print('請輸入正確功能！')
			continue		
		elif msg == '1':
			sel(s,name)
		elif msg == '2':
			his(s,name)
		elif msg == '3':
			return


def sel(s,name):
	while True:
		word = input('請輸入想查詢的單字：')
		if not word or word == '##':
			break
		s.send('S {} {}'.format(name,word).encode())
		data = s.recv(1024).decode()
		l = data.split('**')
		sig = l[0]
		if sig == 'ok':
			info = l[1]
			print(info)
		else:
			print(data)
			break


def his(s,name):
	print(name)
	s.send("H {}".format(name).encode())
	sig = s.recv(1024).decode()
	if sig == 'ok':
		print('--------------歷史紀錄--------------')
		while True:
			data = s.recv(1024).decode()
			if data =='##':
				print('------------------------------------')
				break
			print(data)
	else:
		print('歷史紀錄為空')


def main():
	if len(sys.argv) < 3:
		print('argv is error')
		return
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	ADDR = (HOST,PORT)

	s = socket()
	try:
		s.connect(ADDR)
	except Exception as e:
		print(e)
		return
    
	while True:
		menu_1()
		try:
			cmd = input("請選擇功能>>")
		except Exception as e:
			print('請輸入正確功能！')
			continue
		if cmd not in['1','2','3']:
			sys.stdin.flush() 
			print('請輸入正確功能！')
			continue
		elif cmd == '1':
			re(s)
		elif cmd == '2':
			name = login(s)
			if name:
				login_2(s,name)
			else:
				continue
		elif cmd == '3':
			client_exit(s)
	s.close()


if __name__ == '__main__':
	main()