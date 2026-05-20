import cv2
import face_recognition
import numpy as np

# ── 1. Known faces load karo ──────────────────────────
known_encodings = []
known_names = []

# Apni photo load karo
rohit_img = face_recognition.load_image_file("known_faces/rohit.jpg")
rohit_encoding = face_recognition.face_encodings(rohit_img)[0]

known_encodings.append(rohit_encoding)
known_names.append("Rohit")  # Apna naam yahan likho

print("Known faces loaded!")

# ── 2. Webcam start karo ──────────────────────────────
cap = cv2.VideoCapture(0)
print("Webcam chal raha hai... Q dabao band karne ke liye")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Chhota karo — speed ke liye
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # ── 3. Is frame mein faces dhundo ─────────────────
    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for (top, right, bottom, left), enc in zip(face_locations, face_encodings):
        # ── 4. Known faces se match karo ──────────────
        matches = face_recognition.compare_faces(known_encodings, enc)
        name = "Unknown"

        # Best match dhundo
        distances = face_recognition.face_distance(known_encodings, enc)
        best_idx = np.argmin(distances)
        if matches[best_idx]:
            name = known_names[best_idx]

        # ── 5. Coordinates wapas bado (4x) ────────────
        top, right, bottom, left = top*4, right*4, bottom*4, left*4

        # ── 6. Box aur naam draw karo ─────────────────
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()