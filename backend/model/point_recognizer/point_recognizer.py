import numpy as np
import tensorflow as tf


class PointRecognizer(object):
    def __init__(
        self,
        model_path='backend/model/point_recognizer/point_recognizer.tflite',
        num_threads=1,
    ):
        self.interpreter = tf.lite.Interpreter(model_path=model_path,
                                               num_threads=num_threads)

        self.interpreter.allocate_tensors() #memory
        self.input_details = self.interpreter.get_input_details() #from model
        self.output_details = self.interpreter.get_output_details() #from model

    def __call__(self, landmark_list,):
        input_details_tensor_index = self.input_details[0]['index'] # TF index of first input
        # set input with the data
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        #After the invocation, we can get the output tensor
        result = self.interpreter.get_tensor(output_details_tensor_index)

        # Squeeze will remove the dimension of 1 e.g (1, 2) -> (2,)
        # and argmax will return the index of the max value e.g [0.1, 0.9] -> 1
        result_index = np.argmax(np.squeeze(result))

        return result_index
