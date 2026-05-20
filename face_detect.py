import cv2

# Webcam start karo
cap = cv2.VideoCapture(0)

# Face detector load karo (OpenCV built-in hai)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

print("Webcam chal raha hai... 'Q' dabao band karne ke liye")

while True:
    # Frame capture karo
    ret, frame = cap.read()
    if not ret:
        break

    # Gray image banao — face detection ke liye zaroori
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Faces dhundo
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    # Har face ke around box draw karo
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Face Detected!", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Screen par dikho
    cv2.imshow("AI Assistant - Face Detection", frame)

    # Q dabao toh band ho
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Webcam band ho gaya!")