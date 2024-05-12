import numpy as np
import tensorflow as tf

from config.constants import *


class PointRecognizer(object):
    def __init__(
        self,
        model_path=TFLITE_SAVE_PATH,
        num_threads=NUM_THREADS,
    ):
        self.interpreter = tf.lite.Interpreter(model_path=model_path,
                                               num_threads=num_threads)

        self.interpreter.allocate_tensors() #memory
        self.input_details = self.interpreter.get_input_details() #from model
        self.output_details = self.interpreter.get_output_details() #from model

    def __call__(self, landmark_list,):
        self.interpreter.set_tensor(
            self.input_details[0]['index'],
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        #After the invocation, we can get the output tensor
        result = self.interpreter.get_tensor(self.output_details[0]['index'])

        # Squeeze will remove the dimension of 1 e.g (1, 2) -> (2,)
        # and argmax will return the index of the max value e.g [0.1, 0.9] -> 1
        result_index = np.argmax(np.squeeze(result))

        return result_index
