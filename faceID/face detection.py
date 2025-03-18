import cv2

# Load the pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the input image
image_path = 'camila cabello.jpg'  # Replace with your image file path
image = cv2.imread(image_path)

# Convert the image to grayscale (required by Haar cascades)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Display the output image
cv2.imshow('Face Detection', image)

# Wait for a key press and close the display window
cv2.waitKey(0)
cv2.destroyAllWindows()
