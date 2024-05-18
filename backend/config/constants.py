import os
# PATHS, absolute paths for the project
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
DATASET_PATH = os.path.join(BACKEND_DIR, 'model/point_recognizer', 'points.csv') # Path to the dataset (created by dev_app.py) 
MODEL_CP_SAVE_PATH = os.path.join(BACKEND_DIR, 'model/point_recognizer', 'point_recognizer.keras') # Path to save the model
TEST_MODEL_CP_SAVE_PATH = os.path.join(BACKEND_DIR, 'model/point_recognizer/test_models', 'test_point_recognizer.keras') # Path to save the test model
TFLITE_SAVE_PATH = os.path.join(BACKEND_DIR, 'model/point_recognizer', 'point_recognizer.tflite') # Path to save the tflite model
TEST_TFLITE_SAVE_PATH = os.path.join(BACKEND_DIR, 'model/point_recognizer/test_models', 'test_point_recognizer.tflite') # Path to save the test tflite model
LABELS_PATH = os.path.join(BACKEND_DIR, 'model/point_recognizer', 'point_recognizer_labels.csv') # Path to save the labels
POINTS_SAVE_PATH =  os.path.join(BACKEND_DIR, 'model/point_recognizer', 'points.csv') # Path to save the trained points
CHAPTERS_PATH = os.path.join(BACKEND_DIR, 'utils/learn/chapter_words') # Path to save the chapters

#### train.py file configs
RANDOM_SEED = 42 # for generating train and test data
NUM_CLASSES = 4 # number of labels
FIT_EPOCHS = 1000 # number of epochs to train the model
FIT_BATCH_SIZE = 128 # batch size for training
EVAL_BATCH_SIZE = 128 # batch size for evaluation

#point_recognizer.py file configs
NUM_THREADS = 1 # SHOULD STAY LIKE THIS

#### dev_app.py file configs
CAP_DEVICE = 0 # Camera device number
CAP_WIDTH = 1280 # Camera width
CAP_HEIGHT = 960 # Camera height
STATIC_IMAGE_MODE = True # If True, the app will use the static image instead of the camera TODO: Check it
MIN_DETECTION_CONFIDENCE = 0.75 # Minimum confidence for detection
MIN_TRACKING_CONFIDENCE = 0.5 # Minimum confidence for tracking
HANDS_NUM = 2 # Number of hands to detect
QUIT_KEY = 'q' # Key to quit the app
#### dev.py file configs