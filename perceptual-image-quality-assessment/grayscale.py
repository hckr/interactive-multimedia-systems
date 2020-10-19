import os
import sys
import cv2

original_image = cv2.imread(
        os.path.join(sys.path[0], 'image.png'))
original_image_grayscale = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

cv2.imwrite(os.path.join(sys.path[0], 'image-grayscale.png'), original_image_grayscale)
