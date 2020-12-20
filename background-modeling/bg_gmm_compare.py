import os
import cv2
import collections
import numpy as np

plik = 'video.mp4'
cap = cv2.VideoCapture(os.path.join(os.path.dirname(__file__), plik))


fgbgAdaptiveGaussian = cv2.createBackgroundSubtractorMOG2()

alpha = 0.3
recent_gray_frames = collections.deque(maxlen=5)

_, frame = cap.read()
first_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
recent_gray_frames.append(first_gray)


def background(frames):
    if len(frames) == 1:
        return frames[0]
    return (1 - alpha) * background(frames[:-1]) + alpha * frames[-1]


while True:
    success, frame = cap.read()
    if not success:
      break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    recent_gray_frames.append(gray_frame)
    bg = background(list(recent_gray_frames)).astype(np.uint8)
    fgmask = cv2.absdiff(bg, gray_frame)
    _, fgmask = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)

    fgbgAdaptiveGaussainmask = fgbgAdaptiveGaussian.apply(frame)

    cv2.namedWindow('Background Subtraction', 0)
    cv2.namedWindow('Background Subtraction Adaptive Gaussian', 0)
    cv2.namedWindow('Original',0)

    cv2.imshow('Background Subtraction', fgmask)
    cv2.imshow('Background Subtraction Adaptive Gaussian', fgbgAdaptiveGaussainmask)
    cv2.imshow('Original',frame)

    k = cv2.waitKey(1) & 0xff

    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('Program Closed')
