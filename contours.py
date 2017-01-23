import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()

    # Retrieve grayscale frame with threshold
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_frame, 127, 255, 0)
    threshold = cv2.medianBlur(threshold, 5)

    # Find contours
    filtered, contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate outline of contours
    epsilon = lambda contour: 0.001 * cv2.arcLength(contour, True)
    poly_contours = [cv2.approxPolyDP(contour, epsilon(contour), True) for contour in contours]

    # Draw contours on filtered
    filtered = frame.copy()
    cv2.drawContours(filtered, poly_contours, -1, (0, 255, 0), 3)

    cv2.imshow('Camera', frame)
    cv2.imshow('Threshold', threshold)
    cv2.imshow('Filtered', filtered)

    key = cv2.waitKey(10) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
