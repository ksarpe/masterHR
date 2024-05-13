import cv2 as cv
import numpy as np
import csv
from PIL import Image
import mediapipe as mp
import itertools

from config.constants import *
from model.point_recognizer.point_recognizer import PointRecognizer
from utils.logger import Logger

class ImageProcessor:
    def __init__(self):
        self.log = Logger("ImageProcessor").get_logger()
        self.labels = self.get_labels()
    

    def get_labels(self):
        with open(LABELS_PATH, encoding='utf-8-sig') as f:
          point_recognizer_labels = csv.reader(f)
          point_recognizer_labels = [
              row[0] for row in point_recognizer_labels
          ]
        return point_recognizer_labels

    # It will return dictionary with:
    # - label_name: e.g "hello"
    # - handedness: e.g "Right"
    def process(self, image):
        # Process image
        self.log.info("Processing image")
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=STATIC_IMAGE_MODE,
            max_num_hands=HANDS_NUM,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

        point_recognizer = PointRecognizer()

        image = Image.open(image.stream).convert('RGB')
        image = np.array(image)
        image = cv.flip(image, 1)
        # save this image to file
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # landmark calculation
                landmark_list = calc_landmark_list(image, hand_landmarks)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)

                # Hand landmark classification
                hand_landmark_id = point_recognizer(pre_processed_landmark_list)
        else:
            self.log.error("Hand not detected")
            return{
                "label_name": "Try again",
                "handedness": "None"
            }
        return {
            "label_name": self.labels[hand_landmark_id],
            "handedness": handedness.classification[0].label[0:],
            }

def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Point
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    # Convert to relative coordinates
    # Calculate distance to every point
    # From the base (wrist) point
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