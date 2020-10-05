import sys,getopt
# import xlsxwriter
# import openpyxl
# from openpyxl import load_workbook
from eir_class import eir

import tempfile
# import win32api
# import win32print
import os
import re

import redis
import json

class eir_print:
	def __init__(self, filename,templatefile,targetDir,setting,printer='',container_index=0):
		self.filename = filename
		self.template_file = templatefile
		self.targetDir = targetDir
		self.printer = printer
		self.setting = setting
		self.json = ''
		self.container_index = container_index

	def print(self):
		try:
			only_filename = os.path.split(self.filename)[1]
			head,tail = os.path.splitext(self.filename)
			eir_obj = eir(self.filename,self.printer)
			data = eir_obj.getInfo()
			self.json = data
			print(data)
			# db = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
			db = redis.StrictRedis('192.168.10.102', 6379, charset="utf-8", decode_responses=True)
			# print(data)
			import json
			lpn = data['license']

			lpn = '%s-%s' % (lpn,self.container_index) if self.container_index != 0 else lpn
			print ('LPN = %s' % lpn)

			# ttl =3600 #1hour
			ttl = 60*5 #5mins Change on Sep 11,2020 -- To decrease ttl of key
			db.set(lpn,json.dumps(data) ) #store dict in a hashjson.dumps(json_data)
			db.expire(lpn, ttl) #expire in hour
			db.publish(self.printer.lower(),lpn)
			print ('Print successful!!')
			return True
		except :
			print ('Error on Print')
			


# Comment by Chutchai on Aug 13,2020
# To send json data to N4 print service

		# # print(data)
		# print ('Template file %s' % self.template_file)

		# import win32com.client as win32
		# excel = win32.gencache.EnsureDispatch('Excel.Application')
		# wb = excel.Workbooks.Open(self.template_file)
		# sheet = wb.Worksheets("EIR")
		# for key in self.setting:
		# 	col_range = self.setting[key]
		# 	sheet.Range(col_range).Value = data[key]
		# 	print (key,col_range,data[key])

		# targetFile = self.targetDir + '\\' + os.path.split(self.filename)[1].replace('.','') +'.xlsx'
		# # Check File existing
		# if os.path.exists(targetFile):
		# 	os.remove(targetFile)

		# print ('Target file %s' % targetFile)
		# # xfile.save(targetFile)
		# # xfile.close()
		# sheet.SaveAs(targetFile)
		# # sheet.Close(True)
		# excel.Quit()
		# # excel.Application.Quit()


		# default_printer =  win32print.GetDefaultPrinter()
		# if self.printer == '' :
		# 	curr_printer = default_printer
		# else:
		# 	curr_printer=self.printer
		# 	win32print.SetDefaultPrinter(curr_printer)
		

		# win32api.ShellExecute (
		# 			  0,
		# 			  "print",
		# 			  targetFile,
		# 			  #
		# 			  # If this is None, the default printer will
		# 			  # be used anyway.
		# 			  #
		# 			  '/d:"%s"' % curr_printer,
		# 			  ".",
		# 			  0
		# 			)

		# win32print.SetDefaultPrinter(default_printer) #set default back to original

		# print ('Print successful!!')
		# return True


