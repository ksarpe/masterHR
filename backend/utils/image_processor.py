import cv2 as cv
import numpy as np
import csv
import mediapipe as mp
import itertools

from PIL import Image

from config.constants import *
from model.point_recognizer.point_recognizer import PointRecognizer
    

def get_labels():
    with open(LABELS_PATH, encoding='utf-8-sig') as f:
        point_recognizer_labels = csv.reader(f)
        point_recognizer_labels = [
            row[0] for row in point_recognizer_labels
        ]
    return point_recognizer_labels

# It will return dictionary with:
# - label_name: e.g "hello"
# - handedness: e.g "Right"
def process(image):
    labels = get_labels()
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=STATIC_IMAGE_MODE,
        max_num_hands=HANDS_NUM,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE
    )
    mp_face = mp.solutions.face_detection
    face = mp_face.FaceDetection(
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        model_selection=FACE_MODEL_SELECTION
    )

    point_recognizer = PointRecognizer()

    image = Image.open(image.stream).convert('RGB')
    image = np.array(image)
    image = cv.flip(image, 1)
    
    image.flags.writeable = False
    results = hands.process(image)
    face_results = face.process(image)
    image.flags.writeable = True
    

    if results.multi_hand_landmarks is not None and face_results.detections is not None:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                results.multi_handedness):
            
            landmark_list = calc_landmark_list(image, hand_landmarks)
            pre_processed_landmark_list = pre_process_landmark(
                landmark_list)
            nose_tip_coords = mp_face.get_key_point(face_results.detections[0], mp_face.FaceKeyPoint.NOSE_TIP)
            hand_landmark_id = point_recognizer(nose_tip_coords, pre_processed_landmark_list)
    else:
        return{
            "label_name": "Spróbuj ponownie!",
        }
    return {
        "label_name": labels[hand_landmark_id],
        }

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