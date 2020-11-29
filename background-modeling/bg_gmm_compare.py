import cv2
import numpy as np
kat='.\\'

plik='GoodVision Traffic Counting using Camera Video Analytics #1 .mp4'
#plik='tennis2.mp4'
#plik='M6 Motorway Traffic - YouTube.mp4'
cap = cv2.VideoCapture(kat+'\\'+plik)


fgbgAdaptiveGaussain = cv2.createBackgroundSubtractorMOG2()

_, frame = cap.read()
first_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)

	
while(1):
  ret, frame = cap.read()
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  fgmask = cv2.absdiff(first_gray, gray_frame)
  _, fgmask = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)

  #noisefld=np.random.randn(frame.shape[0],frame.shape[1])
  #frame[:,:,0]=(frame[:,:,0]+10*noisefld).astype('int')
  #frame[:,:,1]=(frame[:,:,1]+10*noisefld).astype('int')
  #frame[:,:,2]=(frame[:,:,2]+10*noisefld).astype('int')
  
  fgbgAdaptiveGaussainmask = fgbgAdaptiveGaussain.apply(frame)
  
  cv2.namedWindow('Background Subtraction',0)
  cv2.namedWindow('Background Subtraction Adaptive Gaussian',0)
  cv2.namedWindow('Original',0)


  cv2.imshow('Background Subtraction',fgmask)
  cv2.imshow('Background Subtraction Adaptive Gaussian',fgbgAdaptiveGaussainmask)
  cv2.imshow('Original',frame)
  
  k = cv2.waitKey(1) & 0xff
  
  if k==ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
print ('Program Closed')

