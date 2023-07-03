import cv2
import dlib
import sys
import numpy as np
from image_processing import ImageProcessing

scaler = 0.3

# Initialize face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Load video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Failed to open video capture.')
    sys.exit()  # Exit the program

ret, frame = cap.read()


class Detection:
    def __init__(self, com_num):
        # Load overlay image
        overlay_path = f'overlay/33-0{com_num}.png'
        global overlay
        overlay = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)
        self.run()

    # Overlay function
    def overlay_transparent(self, background_img, img_to_overlay_t, x, y, overlay_size=None):
        bg_img = background_img.copy()

        # Convert 3 channels to 4 channels
        if bg_img.shape[2] == 3:
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        b, g, r, a = cv2.split(img_to_overlay_t)
        mask = cv2.medianBlur(a, 5)

        h, w, _ = img_to_overlay_t.shape
        roi = bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]

        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

        bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)] = cv2.add(img1_bg, img2_fg)

        # Convert 4 channels to 4 channels
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

        return bg_img

    def run(self):
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame
            frame = cv2.resize(frame, None, fx=0.3, fy=0.3)
            img = frame.copy()

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = detector(gray)

            # Loop through detected faces
            for face in faces:
                # Get facial landmarks
                landmarks = predictor(gray, face)

                # Convert facial landmarks to NumPy array
                shape = np.array([[p.x, p.y] for p in landmarks.parts()])

                # Calculate face center
                center_x, center_y = np.mean(shape, axis=0).astype(np.int)

                # Calculate face size
                face_size = int(max(shape[:, 1]) - min(shape[:, 1]))

                # Draw facial landmarks
                for i in range(shape.shape[0]):
                    x, y = shape[i]
                    cv2.circle(img, (x, y), 2, (255, 255, 255), -1)

                # Overlay image on face
                result = self.overlay_transparent(frame, overlay, center_x, center_y, overlay_size=(face_size, face_size))

            # Display result
            # cv2.imshow('detect', img)
            cv2.imshow('Face Overlay', result)

            # Save image and go to next frame
            if cv2.waitKey(1) == ord('s'):
                cv2.imwrite('./image/photo.jpg', result)
                break

        ImageProcessing()
