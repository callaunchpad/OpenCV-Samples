import cv2
import numpy as np

cap = cv2.VideoCapture(0)

_, prev_frame = cap.read()
prev_frame = cv2.flip(prev_frame, 1)
prev_gray_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(prev_frame)
hsv[..., 1] = 255

while(1):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prev_gray_frame, gray_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, angle = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[..., 0] = angle * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    filtered = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow('Camera', frame)
    cv2.imshow('Filtered', filtered)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    prev_gray_frame = gray_frame
cap.release()
cv2.destroyAllWindows()
