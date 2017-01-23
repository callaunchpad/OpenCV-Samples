import cv2
import numpy as np

camera = cv2.VideoCapture(0)
cv2.namedWindow('Thresholds')

# Create trackbars
def update(value):
    pass
cv2.createTrackbar('Min Hue', 'Thresholds', 0, 180, update)
cv2.createTrackbar('Min Saturation', 'Thresholds', 0, 255, update)
cv2.createTrackbar('Min Value', 'Thresholds', 0, 255, update)
cv2.createTrackbar('Max Hue', 'Thresholds', 180, 180, update)
cv2.createTrackbar('Max Saturation', 'Thresholds', 255, 255, update)
cv2.createTrackbar('Max Value', 'Thresholds', 255, 255, update)

min_color = np.zeros((128, 128, 3), np.uint8)
max_color = np.zeros((128, 128, 3), np.uint8)

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

    # Create min and max color previews
    min_color[:] = min_threshold
    max_color[:] = max_threshold
    min_color = cv2.cvtColor(min_color, cv2.COLOR_HSV2BGR)
    max_color = cv2.cvtColor(max_color, cv2.COLOR_HSV2BGR)

    # Display min and max color previews
    cv2.imshow('Min Color', min_color)
    cv2.imshow('Max Color', max_color)

    # Filter based on HSV threshold values
    mask = cv2.inRange(hsv, min_threshold, max_threshold)
    mask = cv2.medianBlur(mask, 5)

    # Find contours
    filtered, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate outline of contours
    epsilon = lambda contour: 0.001 * cv2.arcLength(contour, True)
    poly_contours = [cv2.approxPolyDP(contour, epsilon(contour), True) for contour in contours]

    # Draw largest contour
    if len(poly_contours) > 0:
        largestContour = max(poly_contours, key = lambda contour: cv2.contourArea(contour))
        filtered = frame.copy()
        cv2.drawContours(filtered, [largestContour], -1, (0, 255, 0), 3)

    cv2.imshow('Camera', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Filtered', filtered)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
