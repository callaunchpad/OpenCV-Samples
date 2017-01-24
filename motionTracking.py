import cv2
import numpy as np

camera = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Apply median blur
    fgmask = cv2.medianBlur(fgmask, 5)

    # Filter frame
    filtered = cv2.bitwise_and(frame, frame, mask = fgmask)

    cv2.imshow('Camera', frame)
    cv2.imshow('Motion Detection', fgmask)
    cv2.imshow('Filtered', filtered)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()

