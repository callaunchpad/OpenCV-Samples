import cv2
import numpy as np

camera = cv2.VideoCapture(0)

query = cv2.imread('images/book.jpg', 0)
sift = cv2.xfeatures2d.SIFT_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

while True:
    _, frame = camera.read()

    kp1, des1 = sift.detectAndCompute(query, None)
    kp2, des2 = sift.detectAndCompute(frame, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # des1 = np.float32(des1)
    # des2 = np.float32(des2)
    matches = flann.knnMatch(des1, des2, k = 2)

    good = []
    for m, n in matches:
        if m.distance <= 0.7 * n.distance:
            good.append(m)
    print(len(good))
    # frame = cv2.drawMatches(query, kp1, frame, kp2, good, None)

    MIN_MATCH_COUNT = 30
    if len(good) > MIN_MATCH_COUNT:
        print('Good match found!')
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        if len(src_pts) > 3 and len(dst_pts) > 3 and len(src_pts) == len(dst_pts):
            M, mask = cv2.findHomography(np.array(src_pts), np.array(dst_pts), cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            h, w = query.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1],[w - 1, 0] ]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            frame = cv2.polylines(frame, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break
