###############################
#                             #
#  Virtual High Speed Camera  #
#                             #
###############################
#
# Author:      Joao Nuno Carvalho
# Date:        26.11.2018
# License:     MIT License   https://opensource.org/licenses/MIT
# Description: This program is an independent implementation of the concepts
#              and ideas of the paper:
#				
#               Virtual Frame Technique:
#               Ultrafast Imaging with Any Camera
#               By Sam Dillavou, Shmuel M Rubinstein, John M Kolinski
#               https://arxiv.org/abs/1811.02936
#
#              With this code you can expand grayscale fotos of a moving event into
#              256 independent binary images.
#              You can also expand frames inside a movie or a movie into a slow
#              motion version.
#
#
# Lib versions:
#   Python 3.6
#   OpenCV 3.x
#   Numpy

# To actiavte the Anaconda enviroment:
#   conda activate opencv_env


import numpy as np
import cv2
import math


def expandFrame(img, delta_threashold=1, bitDepth=8):
	vImglist = []

	# rows,cols = img.shape
	max_x,max_y, chanels = img.shape
	# max_x,max_y = img.shape

	delta = delta_threashold

	# max_value = np.max(img)
	# min_value = np.min(img)
	num_v_frames = int(math.pow(2, bitDepth) / delta) - 1
	curr_th = 0 + delta - 1
	black = np.uint8(0)
	white = np.uint8(255)

	for i in range(0, num_v_frames):
		# Creates virtual black image [ TODO: optimize].
		# imgVirt = np.ones((max_x,max_y,1),np.uint8)*0
		imgVirt = np.where(img <= curr_th, black, white)
		vImglist.append(imgVirt)
		
		#if (-1<i<10) or (250<i<260):
		#print( " i " + str(i) + " curr_th  " + str(curr_th) )

		curr_th += delta

	return vImglist


def chooseChannel(imgA, color):
	# 1 - Get the type of image A that receves in img, grey, RGB, GBR?
	# 2 - Creates a one channel image B with the same resolution.
	# 3 - Copies the chanel from A to Img B.
	# 4 - Return image.

	imgB = imgA.copy()
	# TODO: implement.
	return imgB


def loadPNGImg(path):
	# Load an color image in grayscale
	img = cv2.imread(path)
	return img


def  makeVirtualVideo(virtualFrames, videoPath, speed=20.0):
	# TODO: Make Video from individual frames.
	virtualVideo = None
	height, width, channel = virtualFrames[0].shape
	print("width, height, channel : " + str(width) + " " + str(height) + " " + str(channel))
	# Define the codec and create VideoWriter object.
	fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Lower case.
	#fourcc = cv2.VideoWriter_fourcc('M','J','P','G') # Lower case.
	out = cv2.VideoWriter(videoPath, fourcc, speed, (width, height))


#	font                   = cv2.FONT_HERSHEY_SIMPLEX
#	bottomLeftCornerOfText = (10,height-20)# 500)
#	fontScale              = 0.5
#	fontColor              = (125,125,125)
#	lineType               = 1


	for frame in virtualFrames:



#		cv2.putText(frame,'C: {:7d} Tsec: {:04.6f}'.format(1000000, 10.00013), 
#			bottomLeftCornerOfText, 
#			font, 
#			fontScale,
#			fontColor,
#			lineType)


		# frame2 = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
		out.write(frame) # Write out frame to video
		
		#cv2.imshow('video',frame)
		#cv2.waitKey(0)

	# Release everything when finished
	out.release()

	return virtualVideo


def saveVirtualVideo(virtualVideo):
	pass


def processSingleFrame(pngPath, slowMoviePath):
	imgFrame = loadPNGImg(path=pngPath) # path="./testRectGrey.png"
	imgFrame =  chooseChannel(imgFrame, color='G')
	virtualFrames = expandFrame(imgFrame)

	#for counter, vFrame in enumerate(virtualFrames):
		#cv2.imshow('img Virt' + str(counter) ,vFrame)
		#cv2.waitKey(0)
	#	print("counter " + str(counter))

	virtualVideo  = makeVirtualVideo(virtualFrames, slowMoviePath ) # "./slowMotionTriang.mp4")
	# virtualVideo  = makeVirtualVideo(virtualFrames, "./slowMotionTriang.avi")
	
	# saveVirtualVideo(virtualVideo)


def processVideo(fastVideoPath, slowMoviePath, bitDelta, outVideoSpeed=25.0):
	# 1 - Read imagens from video.
	# 2 - Expand each frame into virtual frames.
	# 3 - Make slow motion video.

	listFastFrames = []

	fVideo = cv2.VideoCapture(fastVideoPath, 0)
	if (fVideo.isOpened()== False): 
		print("Error opening fast movie file!")

	fVideoFPS = fVideo.get(cv2.CAP_PROP_FPS)	
	print("Fast video frame rate: " + str(fVideoFPS))

	# Read until video is completed
	while(fVideo.isOpened()):
		# Capture frame-by-frame
		ret, frame = fVideo.read()
		if ret == False:
			# Error ocurred.
			break
		listFastFrames.append(frame)

	# When everything done, release the video capture object
	fVideo.release()

	# Open writer to file.
	height, width, channel = listFastFrames[0].shape
	print("width, height, channel : " + str(width) + " " + str(height) + " " + str(channel))
	# Define the codec and create VideoWriter object.
	fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Lower case.
	#fourcc = cv2.VideoWriter_fourcc(*'v4l2') # Lower case.
	out = cv2.VideoWriter(slowMoviePath, fourcc, outVideoSpeed, (width, height))

	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (10,height-20)# 500)
	fontScale              = 0.5
	fontColor              = (125,125,125)
	lineType               = 1

	totalFastVideoFrames = len(listFastFrames)

	# Expand each input frame into n virtual frames.
	for counterA, frame in enumerate(listFastFrames):
		#if (channel == 3):
		#	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		virtualFrames = expandFrame(frame, bitDelta)
		partialSlowVideoFrames = len(virtualFrames)
		for counterB, vFrame in enumerate(virtualFrames):
			
			# Write frame number and time.
			vFrameCounter = counterA * partialSlowVideoFrames + counterB  
			totalSlowVideoFrames = totalFastVideoFrames * partialSlowVideoFrames 
			# vFrameCurrentTime = (1 / (fVideoFPS * partialSlowVideoFrames)) * vFrameCounter 
			vFrameCurrentTime = (1 / fVideoFPS ) * (vFrameCounter / partialSlowVideoFrames) 

			# Write text on frame!
			cv2.putText(vFrame,'C: {:7d} Tsec: {:04.6f}'.format(vFrameCounter, vFrameCurrentTime), 
							bottomLeftCornerOfText, 
							font, 
							fontScale,
							fontColor,
							lineType)

			# Write out frame to video
			out.write(vFrame)

	# Close writer to file and Release everything when finished
	out.release()




pathDir = "./img_dump/"

pngPath       = pathDir + "testTriangPoly.png"
slowMoviePath = pathDir + "slowMotionTriangFrame.mp4"
processSingleFrame(pngPath, slowMoviePath)

pngPath       = pathDir + "testCircle.png"
slowMoviePath = pathDir + "slowMotionCircleFrame.mp4"
processSingleFrame(pngPath, slowMoviePath)

fastVideoPath            = pathDir + "fastMotionTriang2.mp4" 
slowMoviePath            = pathDir + "slowMotionTriang2.mp4"
# fastVideoPath            = pathDir + "fastMotionTriang2.avi" 
# slowMoviePath            = pathDir + "slowMotionTriang2.avi"
bitDelta                 = 1
outVSpeedFramesPerSecond = 25.0
processVideo(fastVideoPath, slowMoviePath, bitDelta, outVSpeedFramesPerSecond)




# Problem solving for the codification of video from Numpy array.
# http://answers.opencv.org/question/66545/problems-with-the-video-writer-in-opencv-300/
