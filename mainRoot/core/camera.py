import math
import os
import threading
import time

import cv2
import face_recognition
import numpy as np


def face_confidence(face_distance, face_match_threshold=0.2):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((.1 - linear_val) * math.pow((linear_val - .5) * 2, .2))) * 100
        return str(round(value, 2)) + "%"


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    attended_students = []
    process_current_frame = True
    counter = 0
    stop_flag = False

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir(r'C:\Users\Joxon\PycharmProjects\attendanceChecker\mainRoot\core\media\faces'):
            face_image = face_recognition.load_image_file(
                fr'C:\Users\Joxon\PycharmProjects\attendanceChecker\mainRoot\core\media\faces\{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

    def recognize_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        self.face_names = []
        print('self names', self.face_names)
        print('self names', self.attended_students)

        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = 'Unknown'
            confidence = 'Unknown'
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = face_confidence(face_distances[best_match_index])
            self.face_names.append(f"{name} ({confidence})")
            for name in self.face_names:
                name = name.split('(')[0].replace(' ', '')
                if name.split('.')[0] not in self.attended_students and name in self.known_face_names:
                    if self.counter >= 10:
                        self.attended_students.append(name.split('.')[0])
                        self.counter = 0
                    self.counter += 1

            # if 'john' in self.face_names[0]:
            #     self.known_face_names.remove(self.face_names[0].split('(')[0].replace(' ',''))

    def run_recognition(self):

        video_capture = cv2.VideoCapture(0)

        def worker():
            print(not self.stop_flag)
            while not self.stop_flag:
                ret, frame = video_capture.read()
                print(self.attended_students)
                if self.process_current_frame:
                    self.recognize_faces(frame)
                self.process_current_frame = not self.process_current_frame


        # Start the worker thread
        threading.Thread(target=worker, daemon=True).start()

        while True:
            frame = video_capture.read()[1]

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                name = name.replace('.png', '').replace('.jpg', '')
                cv2.rectangle(frame, (left, top), (right, bottom), [0, 255, 0], 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), [0, 255, 0], -1)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_to_send = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_to_send + b'\r\n')

            if cv2.waitKey(1) == ord('q'):
                self.stop_flag = True
                break
        video_capture.release()
        cv2.destroyAllWindows()

# if __name__ == '__main__':
#     fr = FaceRecognition()
#     fr.run_recognition()
