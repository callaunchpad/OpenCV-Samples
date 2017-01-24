import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Retrieve grayscale frame with threshold
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    gray_frame = cv2.medianBlur(gray_frame, 15)

    # Apply adaptive gaussian threshold
    threshold = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)

    # Invert threshold image
    threshold = cv2.bitwise_not(threshold)

    cv2.imshow('Camera', frame)
    cv2.imshow('Threshold', threshold)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
