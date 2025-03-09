import cv2
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText

class ProctoringSystem:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.alert_sent = False

    def detect_face(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Camera not available!")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('Proctoring System', frame)

            if len(faces) == 0 and not self.alert_sent:
                self.send_alert()
                self.alert_sent = True

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def send_alert(self):
        sender_email = "youremail@example.com"  # Replace with your email
        receiver_email = "admin@example.com"  # Replace with the recipient's email
        password = "yourpassword"  # Use an app password instead of a raw password

        msg = MIMEText("Alert: No face detected during the exam.")
        msg['Subject'] = 'Proctoring Alert'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Change SMTP for different providers
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)
                print("Alert email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")


if __name__ == "__main__":
    proctor = ProctoringSystem()
    proctor.detect_face()
