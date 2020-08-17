import cv2
from PIL import Image
from time import sleep
import time


class face_detection :

	def detect_faces(self,f_cascade, colored_img, scaleFactor = 1.1):
		

		start = time.time()
		
		#just making a copy of image passed, so that passed image is not changed 
		img_copy = colored_img.copy()          

		#convert the test image to gray image as opencv face detector expects gray images
		gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)          

		#let's detect multiscale (some images may be closer to camera than others) images
		faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);          

		#go over list of faces and draw them as rectangles on original colored img
		for (x, y, w, h) in faces:
			cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2) 

		end = time.time()
		print('Face detection time : %s sec(s)' % (end - start))
		if len(faces)>0:
			print ("Face detected")
			detected = True
		else:
			print("Not found face...!!!!!!!")
			detected = False        

		return (detected,img_copy)
		

	def download_img(self):
		start = time.time()
		from io import BytesIO
		# from StringIO import StringIO
		import urllib3
		# from urllib3 import urlretrieve
		http = urllib3.PoolManager()
		# Production Camera
		headers = urllib3.util.make_headers(basic_auth='gate:Gateview2018')
		r = http.request('GET', 
						'http://gate:Gateview2018@192.168.0.191/Streaming/Channels/1/picture',
						preload_content=False,
						headers=headers)

		# Demo Camera
		# headers = urllib3.util.make_headers(basic_auth='gate:lcb12017')
		# r = http.request('GET', 
		# 		'http://gate:lcb12017@192.168.0.64/Streaming/Channels/1/picture',
		# 		preload_content=False,
		# 		headers=headers)

		# r = http.request('GET', 'http://127.0.0.1:8000/media/images/LCB1/2018/4/20/side0.jpg',preload_content=False)
		img = Image.open(BytesIO(r.data))
		# img.save('driver.png')
		# 400,225
		img_thumbnail = img.resize((600,400),Image.ANTIALIAS)
		img_thumbnail.save('img_captured.png')
		end = time.time()
		print('Download time : %s sec(s)' % (end - start))
		return img

	#haarcascade_frontalface_alt
	#haarcascade_lefteye_2splits.xml
	def capture(self,capture_loop = 5):
		
		lbp_face_cascade = cv2.CascadeClassifier('data/haarcascade_lefteye_2splits.xml')
		for i in range(capture_loop):
			img_capture = self.download_img()
			img = cv2.imread('img_captured.png')
			detected,img = self.detect_faces(lbp_face_cascade,img)

			if detected :
				# Save to file for Upload to Web
				# cv2.putText(img,"Hello World!!!", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
				
				# img_capture.save('main_image.jpg')
				# img_capture.resize((400,225),Image.ANTIALIAS).save('thumbnail_image.jpg')
				print('Thanks Bye!!!!!!!')
				break
			sleep(0.5)

		img_capture.save('main_image.jpg')
		img_capture.resize((400,225),Image.ANTIALIAS).save('thumbnail_image.jpg')

# run()

# from numpy import array
# arr = array(img_capture)
# cv2.putText(arr,"Hello World!!!", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

# cv2.imshow('Test Imag', result_img) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows()