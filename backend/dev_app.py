import csv
import copy
import time

import cv2 as cv
import numpy as np

from model.point_recognizer.point_recognizer import PointRecognizer
from utils.logger import Logger
from config.constants import *
from utils.utils import initialize_camera, load_labels, configure_model, calc_landmark_list, pre_process_landmark

def main():
    log = Logger("app.py").get_logger()

    # Some Variables
    log.info("Setting up variables")
    mode = 0
    current_addition = 0
    photo_iterations = PHOTO_ITERATIONS
    current_digit = -1

    # Initialization
    log.info("Initializing camera and models")
    cap = initialize_camera()
    hands, face, mp_face = configure_model()
    point_recognizer_labels = load_labels()
    point_recognizer = PointRecognizer(testing_mode=True) # Initialize the point recognizer on the pre-trained model

    log.info("Steping into main loop")
    while True:
        # Process Key (ESC: end) #################################################
        key = cv.waitKey(10)
        if key == ord(QUIT_KEY):  # ESC
            break
        digit, mode, new_addition = select_mode(key, mode, current_addition)
        current_addition = new_addition # For increasing signs number more than just 0-9, R-R-R click will increase it by 10


        # Automatic photo capture
        # It will wait two seconds and then just set the digit to the clicked one
        # Because digit is set, it will log PHOTO_ITERATIONS times the same digit with photo to csv
        if digit != -1 and photo_iterations == PHOTO_ITERATIONS:
            current_digit = digit
            photo_iterations -= 1
            time.sleep(2)            
        elif photo_iterations < PHOTO_ITERATIONS and photo_iterations > 0:
            time.sleep(0.001)
            digit = current_digit
            photo_iterations -= 1 #decrement only if we added something to the dataset
        elif photo_iterations == 0:
            photo_iterations = PHOTO_ITERATIONS
            if current_digit != -1:
                print(f"Finished taking photos for this label {current_digit}.")
            current_digit = -1

        # Camera capture #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)
        debug_img = copy.deepcopy(image)

        # Detection implementation #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        face_results = face.process(image)
        image.flags.writeable = True

        nose_tip_coords = None
        
        #Process face and find nose tip
        if face_results.detections is not None:
            for detection in face_results.detections:
                nose_tip_coords = mp_face.get_key_point(detection, mp_face.FaceKeyPoint.NOSE_TIP)
                debug_img = draw_nose_tip(debug_img, nose_tip_coords)
        else:
            nose_tip_coords = None                

        #Process hands
        if results.multi_hand_landmarks is not None and nose_tip_coords is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                bounding_box = calc_rect(debug_img, hand_landmarks)
                landmark_list = calc_landmark_list(debug_img, hand_landmarks)
                landmark_list_to_draw = copy.deepcopy(landmark_list) # Had to do it because the function changes the list
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                
                if mode >= 1 and digit != -1: # log to CSV only if we are in record mode and we have a nose ti                       
                    log_to_csv(digit, nose_tip_coords, mode, pre_processed_landmark_list)
                    break

                hand_landmark_id, confidence, confidence_list = point_recognizer(nose_tip_coords, pre_processed_landmark_list, show_confidence=True, confidence_list=key==ord('c'))
                if key == ord('c'):
                    for index, confidence in enumerate(confidence_list):
                        print(f"{point_recognizer_labels[index]}: {round(confidence / 100, 2) * 100}%")

                debug_img = draw_landmarks(debug_img, landmark_list_to_draw)
                debug_img = draw_hand_text(debug_img, bounding_box, handedness, point_recognizer_labels[hand_landmark_id], confidence)

        debug_img = draw_info(debug_img, mode, current_addition, digit)
        cv.imshow('landmark Language Recognition', debug_img)

    cap.release()
    cv.destroyAllWindows()
    log.info("Closed application cleanly")



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


def log_to_csv(digit, nose_tip_corrds, mode, landmark_list):
    nose_list = [nose_tip_corrds.x, nose_tip_corrds.y]
    if mode == 1 and (0 <= digit <= 9999):
        csv_path = POINTS_SAVE_PATH
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([digit, *nose_list, *landmark_list])
    return


def draw_landmarks(image, landmark_points):
    # Colors and thickness
    line_color_black = (0, 0, 0)
    line_color_white = (255, 253, 208)
    thickness_black = 6
    thickness_white = 2
    circle_radius = 5
    circle_radius_large = 8

    # Define connections between joints
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (2, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (17, 18), (18, 19), (19, 20),
        (0, 17)  # Connects the palm to the little finger
    ]

    # Draw lines for each connection
    if landmark_points:
        for start_point, end_point in connections:
            cv.line(image, tuple(landmark_points[start_point]), tuple(landmark_points[end_point]),
                    line_color_black, thickness_black)
            cv.line(image, tuple(landmark_points[start_point]), tuple(landmark_points[end_point]),
                    line_color_white, thickness_white)

    # Draw circles for each landmark point
    for index, landmark in enumerate(landmark_points):
        radius = circle_radius_large if index in [4, 8, 12, 16, 20] else circle_radius
        cv.circle(image, tuple(landmark), radius, line_color_white, -1)  # White filled circle
        cv.circle(image, tuple(landmark), radius, line_color_black, 1)  # Black border

    return image


def draw_hand_text(image, bounding_box, handedness, hand_landmark_text, confidence):
    cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[1] - 22),
                 (0, 0, 0), -1)

    hand_label = handedness.classification[0].label[0:]
    hand_info = f'{hand_label}: {hand_landmark_text}' if hand_landmark_text != "" else hand_label
    confidence_info = f'({confidence}%)'

    text_position = (bounding_box[0] + 5, bounding_box[1] - 4)
    text_font = cv.FONT_HERSHEY_SIMPLEX
    text_scale = 0.6
    base_text_color = (255, 255, 255)  # White color for the base text
    text_thickness = 1
    text_line_type = cv.LINE_AA

    # Determine color based on confidence
    if confidence > 90:
        confidence_color = (0, 255, 0)  # Green
    elif confidence > 70:
        confidence_color = (255, 255, 0)  # Yellow
    else:
        confidence_color = (255, 0, 0)  # Red

    # Put the hand info text in white
    cv.putText(image, hand_info, text_position, text_font, text_scale,
               base_text_color, text_thickness, text_line_type)

    # Calculate the width of the hand info text (to position the confidence part correctly)
    hand_info_size = cv.getTextSize(hand_info, text_font, text_scale, text_thickness)[0]
    confidence_position = (text_position[0] + hand_info_size[0], text_position[1])

    # Put the confidence text in color
    cv.putText(image, confidence_info, confidence_position, text_font, text_scale,
               confidence_color, text_thickness, text_line_type)

    return image


def draw_nose_tip(image, nose_tip):
    if nose_tip is not None:
        x, y = int(nose_tip.x * image.shape[1]), int(nose_tip.y * image.shape[0])
        cv.circle(image, (x, y), 10, (255, 253, 208), -1)
        cv.circle(image, (x, y), 10, (0, 0, 0), 1)
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
