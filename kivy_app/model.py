from jnius import autoclass
import os
import numpy as np
import cv2
import time
from plyer import accelerometer
from kivy.core.text import Label as CoreLabel

ByteBuffer = autoclass('java.nio.ByteBuffer')
class DetectionModel:

    def __init__(self):
        accelerometer.enable()
        self.scores = []
        self.boxes = []
        self.classes = []
        self.timer = 0
        self.last_acc = (0,0,0)
        self.qr_scanned = False
        self.coin_size = 16
        self.coin_x = 100
        self.coin_y = 100

        File = autoclass('java.io.File')
        Interpreter = autoclass('org.tensorflow.lite.Interpreter')
        InterpreterOptions = autoclass('org.tensorflow.lite.Interpreter$Options')

        model_path = File(os.path.join(os.getcwd(), 'model.tflite'))
        options = InterpreterOptions()
        interpreter = Interpreter(model_path, options)
        interpreter.allocateTensors()
        input_output_class = autoclass('org.test.InputOutputClass')

        self.input_output_class = input_output_class()
        self.interpreter = interpreter
        self.labels = ["apple", "pepper", "orange", "onion", "lemon"]
        self.last_result = []

    def get_input_object(self, image):
        input_data = np.expand_dims(image, axis=0)
        input_mean = 127.5
        input_std = 127.5
        input_data = (np.float32(input_data) - input_mean) / input_std
        input_data = ByteBuffer.wrap(input_data.tobytes())
        return self.input_output_class.get_input(input_data)

    def get_output_object(self):
        return self.input_output_class.get_output()

    def interference(self, image):
        inp = self.get_input_object(image)
        outp = self.get_output_object()
        self.interpreter.runForMultipleInputsOutputs(inp, outp)
        scores = outp.get(0)[0]
        boxes = outp.get(1)[0]
        classes = outp.get(3)[0]
        return scores, boxes, classes

    def update_annotation_parameters(self, image):
        image = image[:,:,:3]
        image = cv2.resize(image, (640, 640))
        self.scores, self.boxes, self.classes = self.interference(image)

    def get_results(self, image, image_scale, mirror, image_pos, image_size):
        scores, boxes, classes = self.scores, self.boxes, self.classes
        imH, imW, _ = image.shape
        results = []
        coin_radius = imW//self.coin_size * image_scale[0]
        coin = (self.coin_x, self.coin_y, coin_radius)
        last_result = []
        for i in range(len(scores)):
            if ((scores[i] > 0.9) and (scores[i] <= 1.0)):
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))               
                x = xmin
                y = ymin
                w = xmax - xmin
                h = ymax - ymin
                y = max(image_size[1] -y -h, 0)
                if mirror:
                    x = max(image_size[0] -x -w, 0)
                x = round(x * image_scale[0] + image_pos[0])
                y = round(y * image_scale[1] + image_pos[1])
                w = round(w * image_scale[0])
                h = round(h * image_scale[1])
                object_name = self.labels[int(classes[i])]
                label = CoreLabel(font_size = w//6)
                label.text = f"{object_name}"
                label.refresh()
                last_result.append({"name": object_name, "width": w/(coin_radius*2), "height": h/(coin_radius*2)})
                results.append({"x":x, "y": y,"w": w,"h": h, "t": label.texture})
        self.last_result = last_result
        label_id = CoreLabel(font_size = image_size[0]//18)
        top_coordinates = [0, round(image_size[1] * image_scale[1] + image_pos[1])]
        id_label = {"pos":top_coordinates, "label": label_id}
        return results, coin, id_label

    def annotate(self, image, scale, mirror, image_pos, image_size, optimize=True):
        if optimize is False:
            self.update_annotation_parameters(image)
        elif time.time() - self.timer > 0.05:
            current_acc = accelerometer.acceleration[:3]
            if np.linalg.norm(np.array(self.last_acc) -np.array(current_acc)) < 1:
                self.update_annotation_parameters(image)
            if time.time() - self.timer > 1:
                self.timer = time.time()
                self.last_acc = accelerometer.acceleration[:3]
        results, coin, id_label = self.get_results(image, scale, mirror, image_pos, image_size)
        
        return results, coin, id_label

    def coin_increase(self):
        if self.coin_size > 1:
            self.coin_size -= 0.5
    
    def coin_reduce(self):
        if self.coin_size < 40:
            self.coin_size += 0.5
