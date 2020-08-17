# Command to run 
# python eir_print3.py -i D:\gateout -t D:\gateout\template\EIR_LCMT.xlsx -c COM5

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
import win32print

import win32gui,win32con,win32api,win32ui
# import re
import pyautogui
import re, traceback
import time
import sys
import tempfile
import argparse

from eir_xlsx import eir_print
from face_detect import face_detection

from colorama import init
from colorama import Fore, Back, Style

from capture_camera import capture_image
import threading
import time
from playsound import playsound



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


class cameraThread (threading.Thread):
    def __init__(self, threadID, name, ip,user,password,counter):
        threading.Thread.__init__(self)
        self.threadID 	= threadID
        self.name 		= name
        self.ip 		= ip
        self.user 		= user
        self.password 	= password
        self.counter 	= counter
    def run(self):
        print ("Starting capture %s" % self.name)
        captured = capture_image(self.name,self.ip,self.user,self.password)
        captured.capture(self.counter)
        print ("Finished capture %s" % self.name)

class outSound (threading.Thread):
    def __init__(self, threadID, name, file_name):
    		threading.Thread.__init__(self)
    		self.threadID 	= threadID
    		self.name 		= name
    		self.file_name 	= file_name
			
    def run(self):
    		print ("Playing %s" % self.name)
    		ask_eir(self.file_name)
    		print ("Finish play sound %s " % self.name)

def ask_eir(file_name):
	try:
		playsound(file_name)#'sounds/eir.wav'
	except:
		print ('Error on Asking for EIR function')

# Initial main parameter
camera_name             = 'B1-face'
eir_sound_thread        = outSound(1, 'eir','sounds/eir.wav')
welocom_sound_thread    = outSound(1, 'welcome','sounds/welcome.wav')
camera1_thread          = cameraThread(1, camera_name,"192.168.0.191","gate","Gateview2018", 1)

def main():
	try:
		init(autoreset=True)

		print(Fore.GREEN + 'Print count start : %s' % paper_count)

		secs_between_keys=0.01
		# regex = "Untitled - Notepad"
		# regex = "Microsoft Excel - Book1"
		regex = "Session A - [24 x 80]"
	 
		win = WindowMgr()
		wh = win.find_window(regex)
		if wh == None :
			print ('%s is not opened' % regex )
			sys.exit()

		(x,y,w,h) = win.set_onTop(wh)
		# Start at First page of CTCS program
		pyautogui.press('f12')
		pyautogui.press('f12')
		pyautogui.press('f12')
		pyautogui.press('f12')

		pyautogui.typewrite('1', interval=secs_between_keys) #Work with CTCS
		pyautogui.press('enter')

		pyautogui.typewrite('4', interval=secs_between_keys) #GATE
		pyautogui.press('enter')


		pyautogui.typewrite('2', interval=secs_between_keys) #GATE out
		pyautogui.press('enter')

		# Focus on Call card item
		pyautogui.press('enter')
		import re
		callcard_rex = re.compile("^[0-9]{5}$")


		# Say Ready to process.
		welocom_sound_thread.start()
		welocom_sound_thread.join()

		while True:
			callcard_number = pyautogui.prompt(text='Please scan Call card number :', title='Scan call card Number' , default='')
			if callcard_number == 'quit' or callcard_number == None or callcard_number == 'q' or callcard_number == 'Q'  :
				print ('See you ,Bye Bye..')
				break
			else :
				if not callcard_rex.match(callcard_number) :
					pyautogui.alert(text='Call Card number must be 5 digits',title="Invalid call card number",button='OK')
					continue


				# Delete Ticket File
				# wh = w.find_window(regex)
				(x,y,w,h) = win.set_onTop(wh)
				win.Maximize(wh)
				
				# Fill Call Card
				pyautogui.press('enter')
				pyautogui.typewrite(callcard_number, interval=secs_between_keys)
				pyautogui.press('enter')
				pyautogui.press('enter')

				# Print EIR ,Capture picture and Upload to Server
				print_eir()
				# Finished

				print ('Finished for call card: %s' % callcard_number )
	except:
		f = open("log.txt", "w")
		f.write(traceback.format_exc())
		print(traceback.format_exc())

def print_eir():
	global paper_count
	sleep(0.1)
	for i in range(0,3):
		eirs = glob.glob(working_dir + '\\*.*')
		if len(eirs)>0:
			for eir in eirs:
				target_dir =makeDirectory()
				# filename=  eirs[0]
				filename =  eir
				# head, tail = os.path.split(eirs[0])
				head, tail = os.path.split(eir)
				print ('Found EIR file : %s ' % filename)
				x = eir_print(filename,template_file,target_dir[0],setting_data,printer)
                
                # Capture Image.
				camera1_thread.start()
				camera1_thread.join()  #Waiting till thread is finished. 

				# Print EIR
				result = x.print()

                # Play sound EIR
				eir_sound_thread.start()

                # Capture Image.
				# camera1_thread.start()
				# camera1_thread.join()  #Waiting till thread is finished. 

				# Move file to output folder 
				target_file = target_dir[0] +'\\' + tail
				shutil.move(eir,target_file )

				paper_count = paper_count + 1
				print(Fore.GREEN + 'Print count : %s' % paper_count)

			
				#Upload to Database (Data)
				# result
				if result :
					print ('---Start to send data---')
					r = upload_container('api/gateout/data',x.json)
					# sys.exit()
					if r['successful']:
						upload_image('api/gateout/image',
                                r['container'],
                                r['slug'],
                                '%s.jpg' % camera_name,
                                '%s_thumbnail.jpg' % camera_name)

			# Open Gaet barrier
			print('Open gate on port %s' % com_port)
			open_gate(com_port)
			# # -----------------
			break
		else:
			print ('Not found EIR file : %s' % datetime.now() )

		sleep(0.5)





if __name__ == "__main__":
	# TEmporary Directory
	ldir = tempfile.mkdtemp()
	atexit.register(lambda dir=ldir: shutil.rmtree(ldir))

	parser = argparse.ArgumentParser()

	parser.add_argument('-p','--printer', default='',
						help="Print to printer")

	parser.add_argument('-i', '--input_directory', action=readable_dir, default=ldir)
	parser.add_argument('-b', '--base_directory', action=readable_dir,default='')
	parser.add_argument('-t', '--template_file',default='eir_template.xlsx', help="EIR Template file")
	parser.add_argument('-c', '--com_port',default='COM1', help="COM port for controller")
	args = parser.parse_args()
	
	# fSrcExist=args.master

	# print ('Real path file %s' % os.path.dirname(os.path.abspath(__file__)))

	printer=args.printer
	if printer =='':
		printer = win32print.GetDefaultPrinter()

	import json
	based_dir = args.base_directory 
	if based_dir =='' :
		fname = os.path.dirname(os.path.abspath(__file__))  + "\eir_setting.json"
	else :
		fname = based_dir + "\eir_setting.json"

	# print ("Configuration file on : %s" % fname)

	if os.path.isfile(fname) :
		x = open(fname).read()
		j = json.loads(x)

	# print ('********************************************************************')
	print ('******************* Auto EIR Start***********************************')
	print ('Configuration path: %s' % fname)
	print ('Template EIR file : %s' % args.template_file)
	print ('Working Directory : %s' % args.input_directory)
	print ('Printer : %s' % printer)
	print ('COM port : %s' % args.com_port)
	print ('********************************************************************')

	# make output in working directory
	success_dir=""
	error_dir = ""
	working_dir = args.input_directory
	template_file = args.template_file
	com_port = args.com_port
	setting_data = j
	# print (printer)
	directory= working_dir +"\output"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	# import serial.tools.list_ports as port_list
	# ports = list(port_list.comports())
	# 	for p in ports:
	# 	print(p)

	# --------------------------------

	# spinner = itertools.cycle(['-', '/', '|', '\\'])


# def ask_eir():
# 	try:
# 		# import pyttsx3
# 		# engine = pyttsx3.init()
# 		# engine.say('Rub bai EIR doy kra')
# 		# engine.say('Rub bai EIR doy kra')
# 		# engine.runAndWait()
# 		from playsound import playsound
# 		playsound('sounds/eir.wav')
# 	except:
# 		print ('Error on Asking for EIR function')

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
