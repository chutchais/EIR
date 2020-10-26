import sys,getopt
import datetime

class eir:
	def __init__(self, filename,printer):
		self.filename = filename
		self.printer = printer
		self.container1_exist = False
		self.container2_exist = False
		self.container3_exist = False
		self.container4_exist = False
		self.MTY_exist =False
		self.container_line_number = 0

	# @staticmethod	

	def get_layout_count(self,layout):
		return len(layout)


	def get_line_text(self,layout,line_number):
		i=1
		for lt_obj in layout:
			if isinstance(lt_obj, LTTextBox) :
				if i==line_number :
					# print('--in function--%s' % i)
					x=lt_obj.get_text()
					return x.strip()
				i=i+1
		return ''

	def get_line_string(self,line_no,start_pos):
		return self.text_content[line_no].strip()

	def get_line_string_raw(self,line_no,start_pos):
		return self.text_content[line_no]

	def getInfo(self):
		try:
			# Modify on Oct 21,2020 -- Fix fix error when file containes alian charecter (add errors='ignore')
			with open(self.filename, errors='ignore') as file:
				x = [l.strip() for l in file]

			line_offset = 0
			# plate_text=''
			# damage=''
			# truck_company=''
			# order_date=''
			# container=''
			# line=''
			# imo1=''
			# imo2=''
			# vessel_name=''
			# vessel_code=''
			# voy=''
			# move=''
			# temperature=''
			# pod=''
			# type_text=''
			# iso=''
			# date=''
			# check_date=''
			# checker=''
			# seal1=''
			# seal2=''
			# gross_weight=''
			# booking=''
			# remark=''
			# remark2=''

			for ix,l in enumerate(x):
				print(ix)
				line_data = l.split('    ')

				# if ix ==  2:#if ix ==  2:
				# 	print('Line of Company:',line_data)
				# 	if len(line_data[0].strip()) == 0 :
				# 		line_offset = 2

				# get Company info
				if ix == line_offset+2:
					print (line_data)
					company = line_data[0].strip()
					if company=='':
						print('Not found Company line')
						line_offset=line_offset-1
					# print (company)
				# get Date,Line,Container
				if ix == line_offset+4:
					print (line_data)
					order_date= line_data[0].strip()
					line= line_data[2].strip()
					container= line_data[7].strip()
					# print (order_date,line,container)

				# get vessel code/voy
				if ix == line_offset+6:
					print (line_data)
					tmp_text = line_data[0].strip()
					voy_arry = tmp_text.split(' ')

					imo1=''

					# Add by Chutchai on June 10
					# To Fix Barge EIR -->return blank
					if tmp_text == '':
						vessel_code_voy_text = ''
						vessel_code = ''
						voy = ''
						imo1 = ''
						continue
					# ###########################

					if len(voy_arry) == 0:
						voy = tmp_text

					if len(voy_arry) >0:
						vessel_code_voy_text = voy_arry[len(voy_arry)-1].strip()
						vessel_code = vessel_code_voy_text.split('/')[0]
						voy = vessel_code_voy_text.split('/')[1]
						imo1 = tmp_text.replace(vessel_code_voy_text,'')

				# get Vessel Name,Move, date
				if ix == line_offset+7:
					print ('IX %s :%s' %(ix,line_data))
					date=''
					
					# Added on Sep 11,2020 - To support Flatrack on Midnigth
					if len(line_data) == 5 :
						print('Flatrack on midnight')
						vessel_name= ''#line_data[0].strip()
						move = line_data[0].strip()
						imo2=''
						date = '%s %s' % (line_data[len(line_data)-2].strip(),line_data[len(line_data)-1].strip())
						continue

					# Added Sep 9,2020 -- To support in case transaction on 00 to 01 am
					if len(line_data) == 4 :
						# Barge BMT
						vessel_name = ''
						move = line_data[0].strip()
						imo2 = ''
						date = line_data[len(line_data)-1].strip()
					else :
						move = line_data[5].strip()
						# Comment on Oct 5,2020 -- To fix wrong Move info
						# if move =='':
						# 	move = line_data[4].strip()
						# if move =='':
						# 	move = line_data[3].strip()
						# if move =='':
						# 	move = line_data[2].strip()
						if not ('IN' in move or 'OUT' in move) :
							move = line_data[4].strip()
						if not ('IN' in move or 'OUT' in move) :
							move = line_data[3].strip()
						if not ('IN' in move or 'OUT' in move) :
							move = line_data[2].strip()

						vessel_name= line_data[0].strip()
						imo2=''
						if len(vessel_name.split('/'))>1:
							# print('Mix')
							tmp_imo = vessel_name.split('/')[0].strip()
							tmp_vessel_name = vessel_name.split('/')[1].strip()

							tmp_vessel_arry = tmp_vessel_name.split(' ')

							tmp_imo = '%s / %s' % (tmp_imo,tmp_vessel_arry[0].strip())
							tmp_vessel_name = tmp_vessel_name.replace(tmp_vessel_arry[0].strip(),'')

							vessel_name = tmp_vessel_name.strip()
							imo2 = tmp_imo.strip()
							# print (tmp_imo,tmp_vessel_name)
							move = line_data[3].strip() #'DRY,2DG'
							if move =='':
								move = line_data[2].strip()#1 DG


						date = line_data[len(line_data)-1].strip()
						

					if len(line_data) == 7 :
						print('After midnight')
						vessel_name= line_data[0].strip()
						move = line_data[2].strip()
						imo2=''
						date = '%s %s' % (line_data[len(line_data)-2].strip(),line_data[len(line_data)-1].strip())

					# Added on Oct 16,2020 Version 1.0.1-- To improve to find move in Line data.
					for item in line_data:
						if ('/IN' in item) or ('/OUT' in item) or ('FULL/' in item) or ('EMPTY/' in item) :
							move = item.strip()
					
					# print(vessel_name,move,date)
				# Type ,ISO ,POD
				# Added on Sep 9,2020 -- To assign default value of pod,type_text and iso
				# To fix Flat lack problem.
				
				if ix == line_offset+9:
					pod=''
					type_text=''
					iso=''
					print(line_data)
					temperature=''
					if len(line_data) == 10: #Reefer
						temperature = line_data[0].strip()
						type_text = line_data[2].strip()
						iso = line_data[5].strip()
						pod = line_data[9].strip()

					if len(line_data) == 8: #Dry
						type_text = line_data[0].strip()
						iso = line_data[3].strip()
						pod = line_data[7].strip()
					
					# Added on Sep 9,2020 -- To support Flat rack
					print('Line data:',len(line_data))
					if len(line_data) == 4: #Flat rack
						type_text = line_data[0].strip()
						iso = line_data[len(line_data)-1].strip()
						print(type_text,iso)
						# pod = line_data[7].strip()

					# print (type_text,iso,pod)

				# PlateID,Truck company,booking
				if ix == line_offset+11:
					print (line_data)
					plate_text = line_data[0].strip()
					truck_company = line_data[2].strip()
					booking = line_data[len(line_data)-1].strip()
					# print(booking)

					

				# Gross weight,Seal
				if ix == line_offset+13:
					print(line_data,len(line_data))
					gross_weight = line_data[0].strip()
					if len(line_data)>2:
						seal1 = line_data[2].strip()
					else:
						seal1 = ''

					# sys.exit()
					# print (gross_weight,seal)

				if ix == line_offset+14:
					print(line_data)
					seal2 = line_data[0].strip()

				#Added on Sep 9,2020 -- TO add Remark

				# Damage, remark
				if ix == line_offset+17:
					print (line_data)
					damage=''
					remark=''
					if len(line_data) == 1: #Refee
						remark = line_data[0].strip()
					if len(line_data) == 8: #Dry
						damage = line_data[0].strip()
						remark = line_data[len(line_data)-1].strip()
					
					# Add on Sep 10,2020 -- To fill damage
					if len(line_data) > 1: #With Damage
						damage = line_data[0].strip()
					remark = line_data[len(line_data)-1].strip()
					
					print(remark)

				if ix == line_offset+18:
					print (line_data)
					damage2=''
					remark2=''
					if len(line_data) == 1: #Refee
						remark2 = line_data[0].strip()
					if len(line_data) == 8: #Dry
						damage2 = line_data[0].strip()
						remark2 = line_data[7].strip()
					# print (damage,remark)
				if ix == line_offset+29:
					print (line_data)
					checker = line_data[0].strip()
					check_date = line_data[len(line_data)-1].strip()
					# print (damage,remark)

			if 'A' in plate_text :
				company = 'A0'
			else :
				company = 'B1'

			# Added by Chutchai on Oct 19,2020 -- To replace 'Out of service' to 'Damage'
			# On version 1.0.2
			if damage == 'Out of service':
				damage = 'Damage'
				
			data = {
				"company": truck_company,
				"document":"EIR",
				"printer":self.printer,
				"start": order_date,
				"license":plate_text,
				"containers": [{
					"number":container,
					"line":line,
					"dg":imo1,
					"trans_type":"",
					"vessel_name":vessel_name,
					"vessel_code":vessel_code,
					"terminal":company,
					"voy_in":voy,
					"voy_out":voy,
					"freightkind":move,
					"temperature":temperature,
					"pod":pod,
					"iso_text":type_text,
					"iso_code":iso,
					"order_date" : order_date,
					"gatein_date":date,
					"created": check_date,
					"creator":checker,
					"seal1":seal1,
					"seal2":seal2,
					"gross_weight":gross_weight,
					"damage":damage,
					"booking":booking,
					"remark":remark, #Added on Sep 9,2020 -- Add remark
					"remark2":remark2 #Added on Sep 9,2020 -- Add remark
					}
				]
			}
			return data
		except Exception as e :
			print ('Error on getInfo function',e)
			# Added on Oct 26,2020 -- To return when file is wrong format
			return {}

# N4 print format
# { "company": "OTHER", "company_code": "OTHER", 
# "containers": [ { "category": "[EXPRT]", 
# "changed": "Aug 11, 2020 3:03 PM", "changer": "gab2151", "created": "Aug 11, 2020 3:03 PM", 
# "creator": "gab2151", "damage": "", "dg": "/", "freightkind": "FCL", "gross_weight": "19000.0", 
# "iso_code": "22G1", "iso_text": "20' 8.6 GP", "line": "CKL", "number": "CKLU2053794", 
# "pod": "KRPUS", "position": "02E-07", "seal1": "Z21321451", "seal2": "", 
# "temperature": "", "terminal": "A0", "trans_type": "RE", "vessel_code": "SORN", "vessel_name": "SKY ORION", 
# "voy_in": "2002N", "voy_out": "2002N" } ], 
# "document": "TID", "license": "653215", 
# "printer": "A0BOOTH2", "start": "2020-08-11 15:03:20", "terminal": "A0", "ttl": 2262 }

# For EIR
# vessel,voy,license,company
# container loop
##number,dg ,trans_type(DM,DI --> vessel_name,voy_in , else-->vessel_name,voy_out)
##freightkind,temperature,pod,iso_text,created,iso_code,seal1,gross_weight,damage
##creator,created