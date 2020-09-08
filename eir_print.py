# Command to run 
# python eir_print.py -i D:\gateout -t D:\gateout\template\EIR_LCMT.xlsx -c COM5

import argparse
import os.path
import os
import tempfile
import shutil
import atexit
from datetime import datetime
from time import sleep
import itertools, sys
import time
import threading
from sys import stdin
import glob
# import win32print

# import win32gui,win32con,win32api,win32ui
# import re
import pyautogui
import re, traceback
import time
import sys
import tempfile


from eir_xlsx import eir_print
import platform
# from face_detect import face_detection

# from colorama import init
# from colorama import Fore, Back, Style




class WindowMgr:
	"""Encapsulates some calls to the winapi for window management"""
	settingFile =''

	def __init__ (self):
		"""Constructor"""
		self.hwnd = None

	def find_window(self,title):
		try:
			self.hwnd = win32gui.FindWindow(None, title)
			assert self.hwnd
			return self.hwnd
		except:
			pyautogui.alert(text='Not found program name ' + title + '\n' 
							'Please open program before excute script', title='Unable to open program', button='OK')
			print ('Not found program')
			return None


	def set_onTop(self,hwnd):
		win32gui.SetForegroundWindow(hwnd)
		return win32gui.GetWindowRect(hwnd)



	def Maximize(self,hwnd):
		win32gui.ShowWindow(hwnd,win32con.SW_RESTORE)#, win32con.SW_MAXIMIZE

	def get_mouseXY(self):
		return win32gui.GetCursorPos()

	def set_mouseXY(self):
		import os.path
		import json
		x,y,w,h = win32gui.GetWindowRect(self.hwnd)
		print ('Current Window X : %s  Y: %s' %(x,y))
		fname = 'd:\\ticket\\setting.json'
		if os.path.isfile(fname) :
			dict = eval(open(fname).read())
			x1 = dict['x']
			y1 = dict['y']
			print ('Setting X : %s  Y: %s' %(x1,y1))
		win32api.SetCursorPos((x+x1,y+y1))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x+x1, y+y1, 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x+x1, y+y1, 0, 0)
		print ('Current Mouse X %s' % self.get_mouseXY()[0])
		print ('Current Mouse Y %s' % self.get_mouseXY()[1])


	def saveFirstDataPos(self):
		x,y,w,h = win32gui.GetWindowRect(self.hwnd)
		print ('Window X : %s  Y: %s' %(x,y))
		x1,y1 = self.get_mouseXY()
		print ('Mouse X : %s  Y: %s' %(x1,y1))
		data={}
		data['x'] = x1-x
		data['y'] = y1-y
		# f = open("setting.json", "w")
		# self.settingFile
		f = open('d:\\ticket\\setting.json', "w")
		f.write(str(data))

		f.close()



	def wait(self,seconds=1,message=None):
		"""pause Windows for ? seconds and print
an optional message """
		win32api.Sleep(seconds*1000)
		if message is not None:
			win32api.keybd_event(message, 0,0,0)
			time.sleep(.05)
			win32api.keybd_event(message,0 ,win32con.KEYEVENTF_KEYUP ,0)

	def typer(self,stringIn=None):
		PyCWnd = win32ui.CreateWindowFromHandle(self.hwnd)
		for s in stringIn :
			if s == "\n":
				self.hwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
				self.hwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
			else:
				print ('Ord %s' % ord(s))
				PyCWnd.SendMessage(win32con.WM_CHAR, ord(s), 0)
		PyCWnd.UpdateWindow()


#     import win32ui
# import time

	def WindowExists(windowname):
		try:
			win32ui.FindWindow(None, windowname)

		except win32ui.error:
			return False
		else:
			return True





# url = 'http://127.0.0.1:8000' #Develop 
url = 'http://192.168.10.20:8001' #Production
paper_count = 0 

class readable_dir(argparse.Action):
	def __call__(self,parser, namespace, values, option_string=None):
		prospective_dir=values
		if not os.path.isdir(prospective_dir):
			raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
		if os.access(prospective_dir, os.R_OK):
			setattr(namespace,self.dest,prospective_dir)
		else:
			raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def makeDirectory():
	# print ('make dir')
	# output for today directory
	target_dir =directory + "\\" + "{:%Y-%m-%d}".format(datetime.now())
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)
	success_dir = target_dir +"\\success"
	error_dir = target_dir +"\\error"
	if not os.path.exists(success_dir):
		os.makedirs(success_dir)
	if not os.path.exists(error_dir):
		os.makedirs(error_dir)
	return (success_dir,error_dir)


# def main():
# 	try:
# 		init(autoreset=True)

# 		print(Fore.GREEN + 'Print count start : %s' % paper_count)

# 		secs_between_keys=0.01
# 		# regex = "Untitled - Notepad"
# 		# regex = "Microsoft Excel - Book1"
# 		regex = "Session A - [24 x 80]"
	 
# 		win = WindowMgr()
# 		wh = win.find_window(regex)
# 		if wh == None :
# 			print ('%s is not opened' % regex )
# 			sys.exit()

# 		(x,y,w,h) = win.set_onTop(wh)
# 		# Start at First page of CTCS program
# 		pyautogui.press('f12')
# 		pyautogui.press('f12')
# 		pyautogui.press('f12')
# 		pyautogui.press('f12')

# 		pyautogui.typewrite('1', interval=secs_between_keys) #Work with CTCS
# 		pyautogui.press('enter')

# 		pyautogui.typewrite('4', interval=secs_between_keys) #GATE
# 		pyautogui.press('enter')


# 		pyautogui.typewrite('2', interval=secs_between_keys) #GATE out
# 		pyautogui.press('enter')

# 		# Focus on Call card item
# 		pyautogui.press('enter')
# 		import re
# 		callcard_rex = re.compile("^[0-9]{5}$")


# 		# Say Ready to process.
# 		from playsound import playsound
# 		playsound('sounds/welcome.wav')

# 		while True:
# 			callcard_number = pyautogui.prompt(text='Please scan Call card number :', title='Scan call card Number' , default='')
# 			if callcard_number == 'quit' or callcard_number == None or callcard_number == 'q' or callcard_number == 'Q'  :
# 				print ('See you ,Bye Bye..')
# 				break
# 			else :
# 				if not callcard_rex.match(callcard_number) :
# 					pyautogui.alert(text='Call Card number must be 5 digits',title="Invalid call card number",button='OK')
# 					continue


# 				# Delete Ticket File
# 				# wh = w.find_window(regex)
# 				(x,y,w,h) = win.set_onTop(wh)
# 				win.Maximize(wh)
				
# 				# Fill Call Card
# 				pyautogui.press('enter')
# 				pyautogui.typewrite(callcard_number, interval=secs_between_keys)
# 				pyautogui.press('enter')
# 				pyautogui.press('enter')

# 				# Print EIR ,Capture picture and Upload to Server
# 				print_eir()
# 				# Finished

# 				print ('Finished for call card: %s' % callcard_number )
# 	except:
# 		f = open("log.txt", "w")
# 		f.write(traceback.format_exc())
# 		print(traceback.format_exc())

def main():
	while True:
		print_eir()
		sleep(1)

def print_eir():
	try:
		global paper_count
		file_index = 0
		for i in range(0,4):
			eirs = glob.glob(working_dir + '\\*.*')
			# total_files = len(eirs)-1 #Add on Sep 8,2020 -- to support cycle container
			if len(eirs)>0:
				for eir in eirs:
					target_dir =makeDirectory()
					# filename=  eirs[0]
					filename =  eir
					# head, tail = os.path.split(eirs[0])
					head, tail = os.path.split(eir)
					print ('Found EIR file : %s ' % filename)
					x = eir_print(filename,"",target_dir[0],setting_data,pc_name,file_index)
					file_index = file_index+1

				# 	# Capture Image and do Face Detection
				# 	# Delete Main and Thumbnail image file.
					
				# 	captured = face_detection()
				# 	captured.capture(1)
				# 	# ------------

				# 	# Once face captured then Print EIR
				# 	# ask_eir()
					result = x.print()
					# print(result)
				# 	# ask_eir()
				# 	# Move file to output folder 
					target_file = target_dir[0] +'\\' + tail
					shutil.move(eir,target_file )
					sleep(1)



				# 	paper_count = paper_count + 1
				# 	print(Fore.GREEN + 'Print count : %s' % paper_count)

				# 	# Count up print-out

				# 	# # -----------------
					
				# 	#Upload to Database (Data)

				# 	# result
				# 	if result :
				# 		# captured = face_detection()
				# 		# captured.capture(1)
				# 		print ('---Start to send data---')
				# 		r = upload_container('api/gateout/data',x.json)
				# 		# sys.exit()
				# 		if r['successful']:
				# 			upload_image('api/gateout/image',r['container'],r['slug'],'main_image.jpg','thumbnail_image.jpg')

				# # Say receive EIR
				# ask_eir()

				# # Open Gaet barrier
				# print('Open gate on port %s' % com_port)
				# open_gate(com_port)
				# # # -----------------
				break
			else:
				print ('Not found EIR file : %s' % datetime.now() )
	except :
		pass
	
	sleep(0.5)





if __name__ == "__main__":
	# TEmporary Directory
	ldir = tempfile.mkdtemp()
	atexit.register(lambda dir=ldir: shutil.rmtree(ldir))

	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--input_directory', action=readable_dir, default=ldir)
	args = parser.parse_args()
	

	'---------Added on Nov 21,2019 to get PC name---'
	pc_name = platform.node()
	if pc_name =='':
		pc_name = socket.gethostname()
	if pc_name == '' :
		pc_name=os.environ['COMPUTERNAME']
	# ----------------------------------------------

	
	import json
	fname = "configure.json"
	if os.path.isfile(fname) :
		x = open(fname).read()
		j = json.loads(x)
		print_server = j['print_service']


	print ('******************* Auto EIR Start***********************************')
	print ('Printing Service : %s' % print_server)
	print ('Working Directory : %s' % args.input_directory)
	print ('PC Name : %s' % pc_name)
	# print ('COM port : %s' % args.com_port)
	print ('********************************************************************')

	# make output in working directory
	success_dir=""
	error_dir = ""
	working_dir = args.input_directory
	# template_file = args.template_file
	# com_port = args.com_port
	setting_data = j
	# print (printer)
	directory= working_dir +"\output"
	if not os.path.exists(directory):
		os.makedirs(directory)
	

	# Add by Chutchai on Dec 27,2018
	# To delete all file on Working directory
	# import glob
	# files = glob.glob(working_dir + '\*')

	# for f in files:
	#     if not 'output' in f and not 'template' in f :
	#     	print ('Delete %s' % f)
	#     	os.remove(f)
	# ---------------------------------------



def ask_eir():
	try:
		# import pyttsx3
		# engine = pyttsx3.init()
		# engine.say('Rub bai EIR doy kra')
		# engine.say('Rub bai EIR doy kra')
		# engine.runAndWait()
		from playsound import playsound
		playsound('sounds/eir.wav')
	except:
		print ('Error on Asking for EIR function')

def open_gate(comport):
	try :
		import serial
		import time
		s = serial.Serial(comport)
		time.sleep(7)
		s.write('0'.encode())
		print('Open gate Successful')
	except:
		print ('Error on Comport')
	# finally:
	# 	s.close()

def upload_container(service,data):
	try :
		import urllib3
		http = urllib3.PoolManager()
		import json
		# import requests
		os.environ['NO_PROXY'] = url
		headers = {'Content-type': 'application/json'}
		# headers = urllib3.util.make_headers(basic_auth='admin:lcb12017',content_type='application/json')
		url_service = url + '/' + service 
		print (data)
		r = http.request('POST', url_service,headers=headers,body=json.dumps(data))
		print (r.data)
		return json.loads(r.data.decode('utf-8'))
	except:
		print ('Error on upload_container function')
		return ""

def upload_image(service,container_number,container_slug,image1,image2):
	try :
		import os
		import requests
		print ('Upload files to Web service')
		os.environ['NO_PROXY'] = url
		url_service = url + '/' + service 
		fimg = open(image1, 'rb')
		fthum = open(image2, 'rb')
		files = {'image':('%s.png' % container_number ,fimg),
				'thumbnails':('%s_thumbnail.png' % container_number ,fthum)}
		data = {'slug':container_slug}
		try:
		  r = requests.post(url_service,files=files,data=data)
		  # print (r.text)
		finally:
		  fimg.close()
		  fthum.close()
		# r = requests.post(urls,files=files,data={'slug':'sdsdsd'})

		# files = {'image':('image.png',i),
		# 'thumbnails':('tum.png',t)}
		return json.loads(r.text)
	except:
		print ('Error on upload_image function')
		return ""

main()
