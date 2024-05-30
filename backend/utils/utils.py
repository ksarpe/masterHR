import cv2 as cv
import itertools
import csv
from config.constants import *
import mediapipe as mp

def initialize_camera():
    """Initialize the camera and set properties."""
    cap = cv.VideoCapture(CAP_DEVICE)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)
    return cap

def load_labels(chapter=0):
    """Load classifier labels from a CSV file."""
    path = LABELS_PATH if chapter == 0 else LABELS_PATH2
    with open(path, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        labels = [row[0] for row in reader]
    return labels

def configure_model():
    """Load and configure Mediapipe models for hands and face."""
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=STATIC_IMAGE_MODE,
        max_num_hands=HANDS_NUM,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )
    mp_face = mp.solutions.face_detection
    face = mp_face.FaceDetection(
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        model_selection=FACE_MODEL_SELECTION
    )
    return hands, face, mp_face

def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        landmark_list[index][0] = landmark_list[index][0] - base_x
        landmark_list[index][1] = landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    # ["abc", "def"] -> ["a", "b", "c", "d", "e", "f"]
    landmark_list = list(
        itertools.chain.from_iterable(landmark_list))

    # Normalization
    # Get the furthest landmark from the base
    max_value = max(list(map(abs, landmark_list)))

    # Get the distances in values from -1 to 1 
    landmark_list = list(map(lambda n: n / max_value, landmark_list))

    return landmark_list