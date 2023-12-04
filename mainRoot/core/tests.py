# import threading
#
# import cv2
# from deepface import DeepFace
#
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
#
# class DeepFaceRec:
#     def __init__(self):
#         self.reference_img = cv2.imread(r"C:\Users\Joxon\PycharmProjects\attendanceChecker\mainRoot\core\media\faces"
#                                         r"\kovanskiy3.png")  # use your own image here
#         self.counter = 0
#         self.face_match = False
#
#     def check_face(self, frame):
#         try:
#             if DeepFace.verify(frame, self.reference_img.copy())['verified']:
#                 self.face_match = True
#             else:
#                 self.face_match = False
#         except ValueError:
#             self.face_match = False
#
#     def rec(self):
#         while True:
#             ret, frame = cap.read()
#
#             if ret:
#                 if self.counter % 30 == 0:
#                     try:
#                         threading.Thread(target=self.check_face, args=(frame.copy(),)).start()
#                     except ValueError:
#                         pass
#                 self.counter += 1
#                 if self.face_match:
#                     cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
#                 else:
#                     cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
#
#                 cv2.imshow('video', frame)
#
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame_to_send = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_to_send + b'\r\n')
#
#             key = cv2.waitKey(1)
#             if key == ord('q'):
#                 break
#
#         cv2.destroyAllWindows()




# import threading
# import cv2
# import face_recognition
#
# # Load reference image and encode faces
# reference_image = face_recognition.load_image_file(
#     r"C:\Users\Joxon\PycharmProjects\attendanceChecker\mainRoot\core\media\faces"
#     r"\kovanskiy3.png")
# reference_encoding = face_recognition.face_encodings(reference_image)[0]
#
# # List to store recognized people
# recognized_people = []
#
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
# counter = 0
# face_match = False
#
#
# def check_face(frame):
#     global face_match
#     global recognized_people
#     try:
#         # Find all face locations in the frame
#         face_locations = face_recognition.face_locations(frame)
#         # If there are faces in the frame, check if any match the reference face
#         if face_locations:
#             face_encodings = face_recognition.face_encodings(frame, face_locations)
#             for face_encoding in face_encodings:
#                 if face_recognition.compare_faces([reference_encoding], face_encoding)[0]:
#                     face_match = True
#                     # Get the name of the recognized person (you can change this logic)
#                     name = "John Doe"
#                     # Add the name to the list if not already present
#                     if name not in recognized_people:
#                         recognized_people.append(name)
#         else:
#             face_match = False
#     except ValueError:
#         face_match = False
#
#
# while True:
#     ret, frame = cap.read()
#     if ret:
#         if counter % 30 == 0:
#             try:
#                 threading.Thread(target=check_face, args=(frame.copy(),)).start()
#             except ValueError:
#                 pass
#         counter += 1
#         if face_match:
#             cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
#         else:
#             cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
#
#         # Display recognized people's names
#         if recognized_people:
#             names_text = "Recognized: " + ", ".join(recognized_people)
#             cv2.putText(frame, names_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#
#         cv2.imshow('video', frame)
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break
#
# cv2.destroyAllWindows()
import os
#
print(os.listdir(r'C:\Users\Joxon\PycharmProjects\attendanceChecker\mainRoot\core\media\faces'))