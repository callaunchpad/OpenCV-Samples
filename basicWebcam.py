import cv2

camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(30) & 0xff

    # Exit on escape
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
