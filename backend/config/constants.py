#### train.py file configs
RANDOM_SEED = 42
NUM_CLASSES = 3
FIT_EPOCHS = 1000
FIT_BATCH_SIZE = 128
EVAL_BATCH_SIZE = 128
# paths are relative from the train.py file
DATASET = 'model/point_recognizer/points.csv' # Path to the dataset (created by dev_app.py)
MODEL_CP_SAVE_PATH = 'model/point_recognizer/point_recognizer.hdf5' # Path to save the model
TFLITE_SAVE_PATH = 'model/point_recognizer/point_recognizer.tflite' # Path to save the tflite model

#### dev_app.py file configs
#### dev.py file configs