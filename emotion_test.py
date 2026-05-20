from deepface import DeepFace
import cv2

cap = cv2.VideoCapture(0)
print("Emotion detection chal raha hai... Q dabao band karne ke liye")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # ── Emotion analyze karo ──────────────────────
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False
        )

        # ── Top emotion nikalo ────────────────────────
        emotion = result[0]['dominant_emotion']
        confidence = result[0]['emotion'][emotion]

        # ── Screen par dikhao ─────────────────────────
        text = f"{emotion.upper()} ({confidence:.0f}%)"
        cv2.putText(frame, text, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    except Exception as e:
        cv2.putText(frame, "Detecting...", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()