import csv
import copy
import itertools
import time

import cv2 as cv
import numpy as np
import mediapipe as mp

from model.point_recognizer.point_recognizer import PointRecognizer
from utils.logger import Logger
from config.constants import *

def main():
    log = Logger("app.py").get_logger()

    use_bounding_box = True
    mode = 0
    current_addition = 0
    photo_iterations = PHOTO_ITERATIONS
    current_digit = -1

    # Camera preparation ###############################################################
    log.info("Preparing camera")
    cap = cv.VideoCapture(CAP_DEVICE)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)

    # Model load #############################################################
    log.info("Loading mediapipe model")
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=STATIC_IMAGE_MODE,
        max_num_hands=HANDS_NUM,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )

    point_recognizer = PointRecognizer(testing_mode=True) # Initialize the point recognizer on the pre-trained model

    # Read labels ###########################################################
    log.info("Reading classifier labels")
    # It will read the labels and create a list of them
    with open(LABELS_PATH,
              encoding='utf-8-sig') as f:
        point_recognizer_labels = csv.reader(f)
        point_recognizer_labels = [
            row[0] for row in point_recognizer_labels
        ]

    log.info("Steping into main loop")
    while True:
        # Process Key (ESC: end) #################################################
        key = cv.waitKey(10)
        if key == ord(QUIT_KEY):  # ESC
            break
        digit, mode, new_addition = select_mode(key, mode, current_addition)
        current_addition = new_addition

        if digit != -1 and photo_iterations == PHOTO_ITERATIONS:
            current_digit = digit
            photo_iterations -= 1
            time.sleep(2)
        elif photo_iterations < PHOTO_ITERATIONS and photo_iterations > 0:
            photo_iterations -= 1
            time.sleep(0.001)
            digit = current_digit
        elif photo_iterations == 0:
            photo_iterations = PHOTO_ITERATIONS
            if current_digit != -1:
                print(f"Finished taking photos for this label {current_digit}.")
            current_digit = -1


        # Camera capture #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = np.array(image)
        image = cv.flip(image, 1)
        debug_img = copy.deepcopy(image)

        # Detection implementation #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        #  ####################################################################
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                bounding_box = calc_rect(debug_img, hand_landmarks)
                landmark_list = calc_landmark_list(debug_img, hand_landmarks)
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                if mode >= 1:
                    log_to_csv(digit, mode, pre_processed_landmark_list)
                    break

                hand_landmark_id, confidence = point_recognizer(pre_processed_landmark_list, show_confidence=True)

                debug_img = draw_bounding_rect(use_bounding_box, debug_img, bounding_box)
                debug_img = draw_landmarks(debug_img, landmark_list)
                debug_img = draw_hand_text(debug_img, bounding_box, handedness, point_recognizer_labels[hand_landmark_id], confidence)

        debug_img = draw_info(debug_img, mode, current_addition, digit)
        cv.imshow('landmark Language Recognition', debug_img)

    cap.release()
    cv.destroyAllWindows()


def select_mode(key, mode, addition):
    digit = -1
    if 48 <= key <= 57:  # 0 ~ 9 (If is in 'R(record)' mode then it will log this label point to training set)
        digit = key - 48 + addition
    if key == 110:  # n (Normal mode)
        mode = 0
        addition = 0 # we reset addition
    if key == 114:  # r (Log to training set)
        if mode == 1:
            addition += 10 #we add ten to the addition so if we want to log 10 we can click 0 and it will add 10
        mode = 1
    return digit, mode, addition


def calc_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


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
    temp_landmark_list = copy.deepcopy(landmark_list) #Get the copy of this list

    # Convert to relative coordinates
    # Calculate distance to every point
    # From the base (wrist) point
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    # ["abc", "def"] -> ["a", "b", "c", "d", "e", "f"]
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    # Get the furthest landmark from the base
    max_value = max(list(map(abs, temp_landmark_list)))

    # Get the distances in values from -1 to 1 
    temp_landmark_list = list(map(lambda n: n / max_value, temp_landmark_list))

    return temp_landmark_list


def log_to_csv(digit, mode, landmark_list):
    if mode == 1 and (0 <= digit <= 9999):
        csv_path = POINTS_SAVE_PATH
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([digit, *landmark_list])
    return


def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        # Thumb
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (255, 255, 255), 2)

        # Index finger
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (255, 255, 255), 2)

        # Middle finger
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (255, 255, 255), 2)

        # Ring finger
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (255, 255, 255), 2)

        # Little finger
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (255, 255, 255), 2)

        # Palm
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (255, 255, 255), 2)

    # Key Points
    for index, landmark in enumerate(landmark_point):
        if index == 0:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 1:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 2: 
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 3: 
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 4:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 5: 
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 6:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 7: 
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 8: 
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 9:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 10:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 11:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 12:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 13:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 14:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 15:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 16:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 17: 
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 18:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 19: 
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 20:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

    return image


def draw_bounding_rect(use_bounding_box, image, bounding_box):
    if use_bounding_box:
        cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]),
                     (0, 0, 0), 1)

    return image


def draw_hand_text(image, bounding_box, handedness, hand_landmark_text, confidence):
    cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[1] - 22),
                 (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    if hand_landmark_text != "":
        info_text +=  f':{hand_landmark_text}'
    info_text += f'({confidence}%)'

    text_position = (bounding_box[0] + 5, bounding_box[1] - 4)
    text_font = cv.FONT_HERSHEY_SIMPLEX
    text_scale = 0.6
    text_color = (255, 255, 255)  # White color
    text_thickness = 1
    text_line_type = cv.LINE_AA

    # Place the text on the image
    cv.putText(image, info_text, text_position, text_font, text_scale,
               text_color, text_thickness, text_line_type)

    return image

#TODO: Check the licenses for this code
def draw_info(image, mode, addition, digit):
    status_labels = ["DEBUG", "RECORD"]
    vertical_offset = 30
    text_color = (255, 255, 255)  # White color
    font = cv.FONT_HERSHEY_PLAIN
    font_scale = 1.5
    line_type = cv.LINE_AA
    thickness = 1

    cv.putText(image, f"MODE:{status_labels[mode]}", (10, vertical_offset),
                font, font_scale, text_color, thickness, line_type)
    cv.putText(image, f"ADDITION:{addition}", (10, vertical_offset + 20),
                font, font_scale, text_color, thickness, line_type)
    
    if mode == 1:
        if digit != -1:
            cv.putText(image, f"Currently logging for :{digit}", (10, vertical_offset + 40),
                    font, font_scale, text_color, thickness, line_type)
        else:
            cv.putText(image, f"Currently not logging", (10, vertical_offset + 40),
                    font, font_scale, text_color, thickness, line_type)
    
    return image


if __name__ == '__main__':
    main()
