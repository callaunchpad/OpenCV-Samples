import cv2
import numpy as np

camera = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    _, frame = camera.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.medianBlur(fgmask, 5)

    cv2.imshow('Camera', frame)
    cv2.imshow('Motion Detection', fgmask)

    key = cv2.waitKey(10) & 0xff
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()

