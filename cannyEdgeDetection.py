import cv2

camera = cv2.VideoCapture(0)

cv2.namedWindow('Thresholds')
def update(value):
    pass
cv2.createTrackbar('Threshold 1', 'Thresholds', 0, 200, update)
cv2.createTrackbar('Threshold 2', 'Thresholds', 186, 200, update)

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    filtered = cv2.GaussianBlur(frame, (5, 5), 0)
    edges = cv2.Canny(filtered, cv2.getTrackbarPos('Threshold 1', 'Thresholds'), cv2.getTrackbarPos('Threshold 2', 'Thresholds'))

    cv2.imshow('Camera', frame)
    cv2.imshow('Filter', filtered)
    cv2.imshow('Canny Edge Detection', edges)

    key = cv2.waitKey(30) & 0xff

    # Exit on escape
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
