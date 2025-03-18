import cv2
import face_recognition

# Load and encode known faces
known_image_1 = face_recognition.load_image_file("sanidhya.png")  # Replace with a known person's image
known_image_2 = face_recognition.load_image_file("camila cabello.png")  # Replace with another known person's image
known_encoding_1 = face_recognition.face_encodings(known_image_1)[0]
known_encoding_2 = face_recognition.face_encodings(known_image_2)[0]

# Create lists of known face encodings and their names
known_face_encodings = [known_encoding_1, known_encoding_2]
known_face_names = ["Person 1", "Person 2"]

# Open a connection to the webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not access the webcam.")
    exit()

while True:
    # Capture a frame from the webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize the frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the frame from BGR to RGB (required by face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Detect faces and encode them
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    if len(face_locations) == 0:
        print("No faces detected in the frame.")
        continue
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


    # Initialize a list for face names
    face_names = []

    for face_encoding in face_encodings:
        # Compare the face encoding with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance if there's a match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin() if len(face_distances) > 0 else None
        if best_match_index is not None and matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up the face locations since the frame was resized
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw the label with a name
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("Face Recognition", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
