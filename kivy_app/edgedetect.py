from kivy.graphics import Color, Rectangle, Line
import numpy as np
from camera4kivy import Preview
from model import DetectionModel
from gestures4kivy import CommonGestures
from popup import show_popup

class EdgeDetect(Preview, CommonGestures):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = DetectionModel()
        self.detections = []
        self.auto_analyze_resolution = [640, 640]
        self.coin = ()
        self.test = "ss"
        self.id_label = None
        self.connected_id = None

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
            
        rgba = np.fromstring(pixels, np.uint8).reshape(image_size[1],
                                                         image_size[0], 4)
        detections, coin, id_label = self.model.annotate(rgba, scale, mirror, image_pos, image_size)
        self.detections = detections 
        self.coin = coin
        self.id_label = id_label

    def canvas_instructions_callback(self, texture, tex_size, tex_pos):
        if self.id_label and self.connected_id:
            id_label = self.id_label["label"]
            pos = self.id_label["pos"]
            id_label.text = f"Connected to: {self.connected_id}"
            id_label.refresh()
            Color(0,1,0,1)
            Rectangle(size = id_label.texture.size,
                pos = pos,
                texture = id_label.texture)
        Color(0.83,0.68,0.21,1)
        Line(circle=self.coin)
        for detection in self.detections:
            Color(1,1,1,1)
            Line(rectangle=(detection['x'], detection['y'], detection['w'], detection['h']), width = 3)
            Rectangle(size = detection['t'].size,
                      pos = [(detection['x'] + detection['w'])//2, (detection['y'] + detection['h'])],
                      texture = detection['t'])

    def cg_long_press(self, touch, x, y):
        self.model.coin_x = x
        self.model.coin_y = y
