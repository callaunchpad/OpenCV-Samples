import cv2

camera = cv2.VideoCapture(0)

# Fullscreen
# cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cascades = ['./cascades/haarcascade_frontalface_alt.xml']

def drawText(frame, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (10, 32), font, 1, (0, 255, 0), 3, cv2.LINE_AA)

classifiers = []
for cascade in cascades:
    classifiers.append(cv2.CascadeClassifier(cascade))

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Sharpen actual frame (OPTIONAL)
    # image = gray_frame.copy()
    # gray_frame = cv2.GaussianBlur(image, (5, 5), 5)
    # gray_frame = cv2.addWeighted(image, 1.5, gray_frame, -0.75, 0)

    faces = []
    for classifier in classifiers:
        for rectangle in classifier.detectMultiScale(gray_frame, scaleFactor = 1.1, minNeighbors = 1):
            faces.append(rectangle)

    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    drawText(frame, "Number of Faces: {}".format(len(faces)))

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(60) & 0xff

    # Exit on escape
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
