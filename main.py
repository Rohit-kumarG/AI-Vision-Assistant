import cv2
import face_recognition
import numpy as np
import sqlite3
import pyttsx3
import speech_recognition as sr
import os
import time
from deepface import DeepFace

# ── Voice Engine ──────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

# ── Speech Recognition ────────────────────────────────
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("🎤 Sun raha hoon...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5)
            text  = recognizer.recognize_google(audio, language="en-US")
            print(f"🎤 Aapne kaha: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Listen error: {e}")
            return ""

def ai_reply(user_input, name, emotion):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        speak(f"Hello {name}! How are you doing?")
    elif "how are you" in user_input:
        speak("I am doing great! Thank you for asking.")
    elif "my name" in user_input:
        speak(f"Your name is {name}!")
    elif "emotion" in user_input or "feeling" in user_input or "mood" in user_input:
        speak(f"Right now you look {emotion} to me!")
    elif "time" in user_input:
        current = time.strftime("%I:%M %p")
        speak(f"The current time is {current}")
    elif "bye" in user_input or "goodbye" in user_input:
        speak(f"Goodbye {name}! Have a great day!")
    elif "joke" in user_input:
        speak("Why did the computer go to the doctor? Because it had a virus!")
    elif "your name" in user_input:
        speak("My name is Aria, your personal AI assistant!")
    else:
        speak(f"You said {user_input}. I am still learning more commands!")

# ── Database ──────────────────────────────────────────
def get_db():
    return sqlite3.connect("database/users.db")

def save_user(name, emotion):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name=?", (name,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users (name, last_emotion) VALUES (?,?)", (name, emotion))
    else:
        cur.execute("UPDATE users SET last_emotion=?, last_seen=CURRENT_TIMESTAMP WHERE name=?",
                    (emotion, name))
    conn.commit()
    conn.close()

# ── Known Faces Load ──────────────────────────────────
known_encodings = []
known_names     = []

print("📸 Known faces load ho rahe hain...")
for filename in os.listdir("known_faces"):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join("known_faces", filename)
        img  = face_recognition.load_image_file(path)
        encs = face_recognition.face_encodings(img)
        if encs:
            known_encodings.append(encs[0])
            name = os.path.splitext(filename)[0].capitalize()
            known_names.append(name)
            print(f"  ✅ {name} loaded")
print(f"Total {len(known_names)} user(s) loaded!\n")

# ── Greeting ──────────────────────────────────────────
def make_greeting(name, emotion):
    lines = {
        "happy":    "You look very happy today!",
        "sad":      "You seem sad. Hope you feel better!",
        "angry":    "You look angry. Take a deep breath!",
        "surprise": "You look surprised!",
        "neutral":  "Hope you are having a good day!",
        "fear":     "You look worried. Everything will be fine!",
        "disgust":  "Something bothering you?"
    }
    line = lines.get(emotion, "Hope you are doing well!")
    if name == "Unknown":
        return "Hello! I don't think we have met. Welcome!"
    else:
        return f"Hello {name}! {line}"

# ══════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════
cap = cv2.VideoCapture(0)

greeted_users  = set()
last_seen_time = {}
absence_secs   = 15

current_name    = "Unknown"
current_emotion = "neutral"

print("🤖 AI Assistant ready!")
print("📌 SPACE dabao mic se baat karne ke liye")
print("📌 Q dabao band karne ke liye\n")

speak("AI Assistant is ready. Press space to talk to me!")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb   = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    locs  = face_recognition.face_locations(rgb)
    encs  = face_recognition.face_encodings(rgb, locs)

    for (top, right, bottom, left), enc in zip(locs, encs):

        # Name match
        name    = "Unknown"
        matches = face_recognition.compare_faces(known_encodings, enc)
        if True in matches:
            dists = face_recognition.face_distance(known_encodings, enc)
            best  = np.argmin(dists)
            if matches[best]:
                name = known_names[best]

        current_name = name

        # Emotion detect
        try:
            result          = DeepFace.analyze(frame, actions=['emotion'],
                                               enforce_detection=False, silent=True)
            current_emotion = result[0]['dominant_emotion']
        except:
            current_emotion = "neutral"

        # Save user
        save_user(name, current_emotion)

        # Greet — sirf ek baar
        now = time.time()
        if name in last_seen_time:
            if (now - last_seen_time[name]) > absence_secs:
                greeted_users.discard(name)
        last_seen_time[name] = now

        if name not in greeted_users:
            greeting = make_greeting(name, current_emotion)
            speak(greeting)
            greeted_users.add(name)

        # Screen par draw — NO visits
        top, right, bottom, left = top*4, right*4, bottom*4, left*4
        color = (0,255,0) if name != "Unknown" else (0,0,255)
        cv2.rectangle(frame, (left,top), (right,bottom), color, 2)
        cv2.putText(frame, f"{name} | {current_emotion.upper()}",
                    (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.putText(frame, "SPACE = Talk | Q = Quit",
                (10, frame.shape[0]-15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)
    cv2.putText(frame, "AI Personal Assistant",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("AI Personal Assistant", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord(' '):
        print("\n🎤 Listening mode ON...")
        speak("Yes, I am listening!")
        user_input = listen()
        if user_input:
            ai_reply(user_input, current_name, current_emotion)
        else:
            speak("Sorry, I could not hear you. Please try again.")

cap.release()
cv2.destroyAllWindows()
print("👋 AI Assistant band ho gaya!")