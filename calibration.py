import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()

    # Draw rectangle
    height, width, channels  = frame.shape
    midPoint = (width // 2, height // 2)
    cv2.circle(frame, midPoint, 8, (0, 255, 0), 3)

    # Display color at midpoint
    color = frame[midPoint[1]][midPoint[0]]
    minColor = np.zeros((128, 128, 3), np.uint8)
    minColor[:] = color

    cv2.imshow('Color Preview', minColor)
    cv2.imshow('Camera', frame)

    key = cv2.waitKey(30) & 0xff

    # Exit on escape
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
