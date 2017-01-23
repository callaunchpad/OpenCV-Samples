import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()

    # Retrieve grayscale frame with threshold
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply adaptive gaussian threshold
    _, binary_filter = cv2.threshold(gray_frame.copy(), 127, 255, cv2.THRESH_BINARY)
    _, trunc_filter = cv2.threshold(gray_frame.copy(), 127, 255, cv2.THRESH_TRUNC)

    cv2.imshow('Camera', frame)
    cv2.imshow('Binary Filter', binary_filter)
    cv2.imshow('Trunc Filter', trunc_filter)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
