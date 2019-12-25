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


#登錄
def login(s):
	name = input('請輸入用戶名：')
	#不顯示密碼
	password = getpass.getpass()
	msg = 'L {} {}'.format(name, password)
	#發送 帳戶密碼
	s.send(msg.encode())
	# 接收 服務端確認
	data = s.recv(1024).decode()

	if data == 'ok':
		print('登錄成功')
		return name
	else:
		print('用戶或密碼錯誤')
		return False


#註冊
def re(s):
	while  True:
		#輸入姓名 密碼
		name = input('請輸入用戶註冊名：')
		if (' ' in name):
			print('用戶名不能加空格')
			continue
		if not name :
			print('請輸入正確格式')
			break
		s.send('R {}'.format(name).encode())

		#服務端回覆，確認此用戶名是否存在
		data = s.recv(1024).decode()
		# ok 用戶名可註冊
		if data == 'ok':
			#輸入密碼
			password = getpass.getpass('請輸入密碼：')
			if not password:
				break
			password1 = getpass.getpass('請在輸入一次密碼：')
			if password != password1:
				print('兩次密碼不同,註冊失敗')
				s.send(b'error')
				break

			s.send(password.encode())
			#接收服務端 註冊成功訊息
			msg = s.recv(1024).decode()
			print(msg)
			break
		else:
			print('此用戶已存在')
			continue

		
#退出
def client_exit(s):
	s.send(b'E')
	s.close()
	sys.exit('謝謝使用')


#二級界面
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
		# 查詢				
		elif msg == '1':
			sel(s,name)
		# 歷史紀錄
		elif msg == '2':
			his(s,name)
		# 退出到第一介面
		elif msg == '3':
			return


#查詢單詞
def sel(s,name):
	while True:
		word = input('請輸入想查詢的單字：')
		if not word or word == '##':
			break
		#發送單詞給服務端
		s.send('S {} {}'.format(name,word).encode())
		#接收服務端回應，判斷是否存在 ok**info
		data = s.recv(1024).decode()
		l = data.split('**')
		sig = l[0]
		if sig == 'ok':
			info = l[1]
			print(info)
		else:
			print(data)
			break


#歷史紀錄
def his(s,name):
	print(name)
	s.send("H {}".format(name).encode())
	#接收服務端回應
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

	#創建套接字
	s = socket()
	try:
		s.connect(ADDR)
	except Exception as e:
		print(e)
		return
    
    # 發送連接請求
	while True:
		# 第一階段菜單
		menu_1()

		#輸入請求命令
		try:
			cmd = input("請選擇功能>>")
		except Exception as e:
			print('請輸入正確功能！')
			continue
		if cmd not in['1','2','3']:
			sys.stdin.flush() #清除標準輸入緩衝區
			print('請輸入正確功能！')
			continue
		# 註冊
		elif cmd == '1':
			re(s)
			#想直接跳轉到二級界面，返回name直接調用
			#login_2(s,name)
		# 登錄
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