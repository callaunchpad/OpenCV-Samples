import cv2
import numpy as np

camera = cv2.VideoCapture(0)

# Helper Functions
def drawText(frame, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (10, 24), font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

# Calculate midpoint
_, frame = camera.read()
height, width, channels = frame.shape
# (column, row)
midPoint = (width // 2, height // 2)

# Calculate tracking window
sideLength = min(width, height) // 4
topLeft = midPoint[0] - sideLength, midPoint[1] - sideLength
bottomRight = midPoint[0] + sideLength, midPoint[1] + sideLength
trackingWindow = topLeft[0], topLeft[1], sideLength, sideLength

# Initialization
while True:
    _,frame = camera.read()

    # Draw rectangle
    cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 0), 3)

    drawText(frame, 'Press spacebar to begin tracking')
    cv2.imshow('Camera', frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27 or key == 32:
        break

# Setup ROI for tracking
# ROI = rectangle of interest
roi = frame[topLeft[1] : topLeft[1] + sideLength, topLeft[0] : topLeft[0] + sideLength]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0.0, 60.0, 32.0)), np.array((180.0, 255., 255.)))
prev_roi = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(prev_roi, prev_roi, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria: 10 iterations or 1 point of movement
termCrit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    _, frame = camera.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    dst = cv2.calcBackProject([hsv], [0], prev_roi, [0, 180], 1)
    _, trackingWindow = cv2.CamShift(dst, trackingWindow, termCrit)

    topLeft = trackingWindow[0], trackingWindow[1]
    bottomRight = topLeft[0] + trackingWindow[2], topLeft[1] + trackingWindow[3]
    cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 0), 3)
    cv2.imshow('Camera', frame)

    key = cv2.waitKey(30) & 0xff

    # Exit on escape
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
