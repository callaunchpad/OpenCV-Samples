import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Parameters for ShiTomasi Corner Detection
feature_params = dict(maxCorners = 100, qualityLevel = 0.3, minDistance = 7, blockSize = 7)

# Parameters for Lucas Kanade Optical Flow
lk_params = dict(winSize = (15, 15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create random colors
color = np.random.randint(0, 255, (100, 3))

# Retrieve first frame and identify corners
_, prev_frame = cap.read()
prev_gray_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(prev_gray_frame, mask = None, **feature_params)

# Create mask image for drawing
mask = np.zeros_like(prev_frame)

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray_frame, gray_frame, p0, None, **lk_params)

    # Select good feature points
    current_features = p0[st == 1]
    next_features = p1[st == 1]

    # Draw the tracks
    for i, (next_feature, current_feature) in enumerate(zip(next_features, current_features)):
        s1, s2 = next_feature.ravel()
        e1, e2 = current_feature.ravel()
        mask = cv2.line(mask, (s1, s2), (e1, e2), color[i].tolist(), 2)
        frame = cv2.circle(frame, (s1, s2), 5, color[i].tolist(), -1)
        img = cv2.add(frame, mask)

    cv2.imshow('Camera', img)

    # Update previous frame and previous points
    prev_gray_frame = gray_frame.copy()
    p0 = next_features.reshape(-1, 1, 2)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cv2.destroyAllWindows()
cap.release()
