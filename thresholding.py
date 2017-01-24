import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Retrieve grayscale frame with threshold
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    median_gray_frame = cv2.medianBlur(gray_frame, 5) 

    # Apply global thresholds
    _, binary_filter = cv2.threshold(median_gray_frame.copy(), 127, 255, cv2.THRESH_BINARY)
    _, trunc_filter = cv2.threshold(median_gray_frame.copy(), 127, 255, cv2.THRESH_TRUNC)

    # Apply adaptive gaussian threshold
    adaptive_threshold = cv2.adaptiveThreshold(median_gray_frame.copy(), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    adaptive_threshold = cv2.bitwise_not(adaptive_threshold)

    # Apply gaussian blur
    gaussian_gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0) 

    # Apply Otsu threshold
    _, otsu_threshold = cv2.threshold(gaussian_gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imshow('Camera', frame)
    cv2.imshow('Binary Filter', binary_filter)
    cv2.imshow('Trunc Filter', trunc_filter)
    cv2.imshow('Adaptive Threshold', adaptive_threshold)
    cv2.imshow('Otsu Threshold', otsu_threshold)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
