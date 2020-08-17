import cv2
from PIL import Image
from time import sleep
import time
import urllib3


class capture_image :
	def __init__(self,camera_name, IP, user_name, password):
    		# threading.Thread.__init__(self)
		self.camera_name 	= camera_name
		self.ip 			= IP
		self.user_name  	= user_name
		self.password 		= password

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
		# import urllib3
		http = urllib3.PoolManager()
		# Production Camera
		headers = urllib3.util.make_headers(basic_auth='%s:%s'%(self.user_name,self.password))
		url = 'http://%s/Streaming/Channels/1/picture' % (self.ip )
		r = http.request('GET', 
						url,
						preload_content=False,
						headers=headers)
		img = Image.open(BytesIO(r.data))
		img_thumbnail = img.resize((600,400),Image.ANTIALIAS)
		img_thumbnail.save('%s.png' % self.camera_name)
		end = time.time()
		print('Download time : %s sec(s)' % (end - start))
		return img

	#haarcascade_frontalface_alt
	#haarcascade_lefteye_2splits.xml
	def capture(self,capture_loop = 5):
		img_capture = self.download_img()
		img_capture.save('%s.jpg' % self.camera_name)
		img_capture.resize((400,225),Image.ANTIALIAS).save('%s_thumbnail.jpg'% self.camera_name)
		return '%s.jpg' % self.camera_name,'%s_thumbnail.jpg'% self.camera_name

		# # lbp_face_cascade = cv2.CascadeClassifier('data/haarcascade_lefteye_2splits.xml')

		# for i in range(capture_loop):
		# 	img_capture = self.download_img()
		# 	# img = cv2.imread('img_captured.png')
		# 	# detected,img = self.detect_faces(lbp_face_cascade,img)
		# 	detected = True
		# 	if detected :
		# 		print('Thanks Bye!!!!!!!')
		# 		break
		# 	sleep(0.5)

		# img_capture.save('main_image.jpg')
		# img_capture.resize((400,225),Image.ANTIALIAS).save('thumbnail_image.jpg')
