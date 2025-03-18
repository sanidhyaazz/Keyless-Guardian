import cv2
import face_recognition

# Load and encode known faces
known_image_1 = face_recognition.load_image_file("sanidhya.png")  # Replace with a known person's image
known_image_2 = face_recognition.load_image_file("camila cabello.png")  # Replace with another known person's image
known_encoding_1 = face_recognition.face_encodings(known_image_1)[0]
known_encoding_2 = face_recognition.face_encodings(known_image_2)[0]

print(known_encoding_1)