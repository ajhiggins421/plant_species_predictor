import glob
from tensorflow import keras
import os
import numpy as np
import cv2
import config


class Classifier:
    def __init__(self):
        self.weight_locations = os.path.join(config.APP_ROOT, "models\\")
        self.model_string_names = glob.glob(f'{self.weight_locations}/*.h5')
        self.model_name_to_index = {}
        self.temp_folder = config.TEMP_FOLDER
        self.model_list = self.load_models()

    def load_models(self):
        model_list = []
        for j, weight in enumerate(self.model_string_names):
            self.model_name_to_index[weight[len(self.weight_locations):-8]] = j
        # load each model
        for weight in self.model_string_names:
            model_list.append(keras.models.load_model(weight))
        return model_list

    def get_prediction_for_image(self, image):
        predictions = []
        image = cv2.imread(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (128, 128))

        for j, model in enumerate(self.model_list):
            predictions.append((self.model_string_names[j][len(self.weight_locations):-8],
                                model.predict(np.array([image]), verbose=0)))

        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[0][0]
