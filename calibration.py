import cv2
import numpy as np

camera = cv2.VideoCapture(0)
cv2.namedWindow('Thresholds')

# Helper Functions
def drawText(frame, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (10, 24), font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

# Initialization
while True:
    _,frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Calculate midpoint
    height, width, channels  = frame.shape
    midPoint = (width // 2, height // 2)

    # Draw circle
    cv2.circle(frame, midPoint, 8, (0, 255, 0), 3)

    drawText(frame, 'Press spacebar to begin calibration')
    cv2.imshow('Camera', frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27 or key == 32:
        break

# Initialize range
_, frame = camera.read()
frame = cv2.flip(frame, 1)
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
height, width, channels  = hsv_frame.shape
midPoint = (width // 2, height // 2)
minColor = hsv_frame[midPoint[1]][midPoint[0]].copy()
maxColor = hsv_frame[midPoint[1]][midPoint[0]].copy()

# Create trackbars
def update(value):
        pass
cv2.createTrackbar('Min Hue', 'Thresholds', 0, 180, update)
cv2.createTrackbar('Min Saturation', 'Thresholds', 0, 255, update)
cv2.createTrackbar('Min Value', 'Thresholds', 0, 255, update)
cv2.createTrackbar('Max Hue', 'Thresholds', 180, 180, update)
cv2.createTrackbar('Max Saturation', 'Thresholds', 255, 255, update)
cv2.createTrackbar('Max Value', 'Thresholds', 255, 255, update)

# Calibration
while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Calculate midpoint
    height, width, channels  = frame.shape
    midPoint = (width // 2, height // 2)

    # Draw circle
    cv2.circle(frame, midPoint, 8, (0, 255, 0), 3)

    # Get HSV color at midpoint
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color = hsv_frame[midPoint[1]][midPoint[0]]

    # Display color at midpoint
    displayColor = np.zeros((128, 128, 3), np.uint8)
    displayColor[:] = frame[midPoint[1]][midPoint[0]]
    cv2.imshow('Color Preview', displayColor)

    # Display min color threshold
    displayColor[:] = minColor
    displayColor = cv2.cvtColor(displayColor, cv2.COLOR_HSV2BGR)
    cv2.imshow('Min Color', displayColor)

    # Display max color threshold
    displayColor[:] = maxColor
    displayColor = cv2.cvtColor(displayColor, cv2.COLOR_HSV2BGR)
    cv2.imshow('Max Color', displayColor)

    cv2.imshow('Camera', frame)

    # Update color thresholds
    for i in range(3):
        minColor[i] = min(minColor[i], color[i])
        maxColor[i] = max(maxColor[i], color[i])

    # Update trackbars
    cv2.setTrackbarPos('Min Hue', 'Thresholds', minColor[0])
    cv2.setTrackbarPos('Min Saturation', 'Thresholds', minColor[1])
    cv2.setTrackbarPos('Min Value', 'Thresholds', minColor[2])
    cv2.setTrackbarPos('Max Hue', 'Thresholds', maxColor[0])
    cv2.setTrackbarPos('Max Saturation', 'Thresholds', maxColor[1])
    cv2.setTrackbarPos('Max Value', 'Thresholds', maxColor[2])

    key = cv2.waitKey(30) & 0xff

    # Exit on escape
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
