import cv2 as cv
import numpy as np

from PIL import Image

from config.constants import *
from utils.utils import load_labels, configure_model, calc_landmark_list, pre_process_landmark
from model.point_recognizer.point_recognizer import PointRecognizer

# It will return dictionary with:
# - label_name: e.g "hello"
def process(image, chapter=0):
    labels = load_labels() if chapter == 0 else load_labels(chapter=2)
    hands, face, mp_face = configure_model()
    point_recognizer = PointRecognizer(chapter_number=2)

    image = Image.open(image.stream).convert('RGB')
    image = np.array(image)
    image = cv.flip(image, 1)
    
    image.flags.writeable = False
    results = hands.process(image)
    face_results = face.process(image)
    image.flags.writeable = True
    

    if results.multi_hand_landmarks is not None and face_results.detections is not None:
        for hand_landmarks, _ in zip(results.multi_hand_landmarks,
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