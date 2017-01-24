import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    box = cv2.blur(frame.copy(), (15, 15))
    gaussian = cv2.GaussianBlur(frame.copy(), (15, 15), 0)
    median = cv2.medianBlur(frame.copy(), 15)
    bilateral = cv2.bilateralFilter(frame.copy(), 9, 75, 75)

    cv2.imshow('Camera', frame)
    cv2.imshow('Box Filter', box)
    cv2.imshow('Gaussian Blur', gaussian)
    cv2.imshow('Median Filter', median)

    key = cv2.waitKey(30) & 0xff

    # Exit on escape
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
