import cv2 as cv
import numpy as np
from PIL import Image
import mediapipe as mp

from config.constants import *
from model.point_recognizer.point_recognizer import PointRecognizer
from utils.logger import Logger

class ImageProcessor:
    def __init__(self):
        self.log = Logger("ImageProcessor").get_logger()

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

        image = Image.open(image.stream)
        image = np.array(image)
        image = cv.flip(image, 1)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        # image.flags.writeable = False
        # results = hands.process(image)
        # image.flags.writeable = True

        # if results.multi_hand_landmarks is not None:
        #     for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
        #                                           results.multi_handedness):
        #         # landmark calculation
        #         landmark_list = calc_landmark_list(debug_img, hand_landmarks)

        #         # Conversion to relative coordinates / normalized coordinates
        #         pre_processed_landmark_list = pre_process_landmark(
        #             landmark_list)

        #         # Hand landmark classification
        #         hand_landmark_id = point_recognizer(pre_processed_landmark_list)

        #         # Drawing part
        #         debug_img = draw_bounding_rect(use_bounding_box, debug_img, bounding_box)
        #         debug_img = draw_landmarks(debug_img, landmark_list)
        #         debug_img = draw_hand_text(
        #             debug_img,
        #             bounding_box,
        #             handedness,
        #             point_recognizer_labels[hand_landmark_id],
        #         )

        # Screen reflection #############################################################
        cv.imshow('landmark Language Recognition', image)
        return 1