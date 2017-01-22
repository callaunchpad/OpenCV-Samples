import cv2
import numpy as np

camera = cv2.VideoCapture(0)
cv2.namedWindow('Thresholds')

# Create trackbars
def update(value):
    pass
cv2.createTrackbar('Min Hue', 'Thresholds', 0, 255, update)
cv2.createTrackbar('Min Saturation', 'Thresholds', 0, 255, update)
cv2.createTrackbar('Min Value', 'Thresholds', 0, 255, update)
cv2.createTrackbar('Max Hue', 'Thresholds', 255, 255, update)
cv2.createTrackbar('Max Saturation', 'Thresholds', 255, 255, update)
cv2.createTrackbar('Max Value', 'Thresholds', 255, 255, update)

while True:
    _, frame = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Update trackbar values
    min_hue = cv2.getTrackbarPos('Min Hue', 'Thresholds')
    min_sat = cv2.getTrackbarPos('Min Saturation', 'Thresholds')
    min_value = cv2.getTrackbarPos('Min Value', 'Thresholds')
    max_hue = cv2.getTrackbarPos('Max Hue', 'Thresholds')
    max_sat = cv2.getTrackbarPos('Max Saturation', 'Thresholds')
    max_value = cv2.getTrackbarPos('Max Value', 'Thresholds')

    min_hue, max_hue = min(min_hue, max_hue), max(min_hue, max_hue)
    min_sat, max_sat = min(min_sat, max_sat), max(min_sat, max_sat)
    min_value, max_value = min(min_value, max_value), max(min_value, max_value)

    min_threshold = np.array([min_hue, min_sat, min_value])
    max_threshold = np.array([max_hue, max_sat, max_value])

    # Filter based on HSV threshold values
    mask = cv2.inRange(hsv, min_threshold, max_threshold)
    filtered = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow('Camera', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Filtered', filtered)

    key = cv2.waitKey(10) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
