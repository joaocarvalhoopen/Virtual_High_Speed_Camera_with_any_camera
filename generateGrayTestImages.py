###############################
#                             #
#  Virtual High Speed Camera  #
#                             #
###############################
#
# Author:      Joao Nuno Carvalho
# Date:        26.11.2018
# License:     MIT License   https://opensource.org/licenses/MIT
# Description: This program generates test data (grey images and gray video)
#              to the program that implements the virtual high speed camera
#              with a normal camera.
#
# Lib versions:
#   Python 3.6
#   OpenCV 3.x
#   Numpy
#
# Ubuntu
#   sudo apt-get install ffmpeg
# 
# To actiavte the Anaconda enviroment:
#  conda activate opencv_env


import numpy as np
import cv2


def createTestRectangle():
	img_size_x = 305
	img_size_y = 300

	min_x = 0
	min_y = 50
	max_x = 1
	max_y = 250
	# Draw image all white(background).
	img1 = np.ones((img_size_x,img_size_y,1),np.uint8)*255
	for x in range(0, 254):
		img2 = np.ones((img_size_x,img_size_y,1),np.uint8)*0
		pt1 = (int(min_x), int(min_y))
		pt2 = (int(max_x+x), int(max_y))
		cv2.rectangle(img2, pt1, pt2, 1, cv2.FILLED)
		img1 -= img2
	return img1 


def createTestTrianglePoly():
	img_size_x = 305
	img_size_y = 300

	min_x = 0
	min_y = 50
	max_x = 1
	max_y = 250
	
	# Draw image all white(background).
	img1 = np.ones((img_size_x,img_size_y,1),np.uint8)*255

	for x in range(0, 254):
		# Image with all zeros.
		img2 = np.ones((img_size_x,img_size_y,1),np.uint8)*0
		pt1 = (int(min_x), int(min_y))
		pt2 = (int(min_x+x), int(min_y))
		pt3 = (int(min_x+x+50), int(min_y+(max_y-min_y)/2))
		pt4 = (int(min_x+x), int(max_y))
		pt5 = (int(min_x), int(max_y))
		contours = np.array( [ pt1, pt2, pt3, pt4, pt5 ] )
		cv2.fillPoly(img2, pts=[contours], color=(1))
		img1 -= img2
	return img1


def createTestCircle(imgType='normal'):
	if imgType == 'normal':
		img_size_x = 305
		img_size_y = 300
	elif imgType == 'full':
		img_size_x = int(256*2)
		img_size_y = int(256*2)
	center_x = int(img_size_x/2)
	center_y = int(img_size_y/2)
	# Draw image all white(background).
	img1 = np.ones((img_size_x,img_size_y,1),np.uint8)*255
	for r in range(0, 254):
		img2 = np.ones((img_size_x,img_size_y,1),np.uint8)*0
		cv2.circle(img2,(center_x, center_y), r, 1, -1)
		img1 -= img2
	return img1 


def drawTestRectangle():
	imgRect = createTestRectangle()
	cv2.imshow('imgRectangle',imgRect)
	cv2.waitKey(0)


def drawTestTrianglePoly():
	imgTriang = createTestTrianglePoly()
	cv2.imshow('imgTriangle',imgTriang)
	cv2.waitKey(0)


def drawTestCircle(imgType='normal'):
	imgCircle = createTestCircle(imgType)
	cv2.imshow('imgCircle', imgCircle)
	cv2.waitKey(0)


def saveAllTestImagesToFileGrey(pathDir):
	imgRect = createTestRectangle()
	cv2.imwrite(pathDir+'testRectGrey.png',imgRect)
	imgTriang = createTestTrianglePoly()
	cv2.imwrite(pathDir+'testTriangPoly.png',imgTriang)
	imgCircle = createTestCircle(imgType='normal')
	cv2.imwrite(pathDir+'testCircle.png',imgCircle)
	imgCircleFull = createTestCircle(imgType='full')
	cv2.imwrite(pathDir+'testCircleFull.png',imgCircleFull)


def  saveVirtualVideo(virtualFrames, videoPath, speed=25.0):
	# Make Video from individual frames.
	height, width, channel = virtualFrames[0].shape
	print("width, height, channel : " + str(width) + " " + str(height) + " " + str(channel))
	# Define the codec and create VideoWriter object.
	fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Lower case.
	# fourcc = cv2.VideoWriter_fourcc(*'ffv1') # Lower case.
	out = cv2.VideoWriter(videoPath, fourcc, speed, (width, height), 0)	 
	for frame in virtualFrames:
		#frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
		out.write(frame) # Write out frame to video
	# Release everything when finished
	out.release()


def saveAllTestVideosImagesToFileGrey(pathDir):
	imgRect = createTestRectangle()
	virtualFrames = [imgRect, imgRect]
	saveVirtualVideo(virtualFrames, pathDir+"fastMotionRect2.mp4", speed=25.0)
	
	imgTriang = createTestTrianglePoly()
	virtualFrames = [imgTriang, imgTriang]
	#saveVirtualVideo(virtualFrames, pathDir+"fastMotionTriang2.mp4", speed=25.0)
	saveVirtualVideo(virtualFrames, pathDir+"fastMotionTriang2.avi", speed=25.0)
	
	imgCircle = createTestCircle(imgType='normal')
	virtualFrames = [imgCircle, imgCircle]
	saveVirtualVideo(virtualFrames, pathDir+"fastMotionCircl2.mp4", speed=25.0)
	
	
	imgCircleFull = createTestCircle(imgType='full')
	virtualFrames = [imgCircleFull, imgCircleFull]
	saveVirtualVideo(virtualFrames, pathDir+"fastMotionCirclFull2.mp4", speed=25.0)


# main
drawTestRectangle()
drawTestTrianglePoly()
drawTestCircle()
drawTestCircle(imgType='full')

pathDir = "./img_dump/"
saveAllTestImagesToFileGrey(pathDir)
saveAllTestVideosImagesToFileGrey(pathDir)

cv2.destroyAllWindows()

