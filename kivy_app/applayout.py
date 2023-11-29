from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from edgedetect import EdgeDetect
import webbrowser
from popup import show_popup
import base64
import json
from kivy.storage.jsonstore import JsonStore
import requests

store = JsonStore('token.json')

class AppLayout(FloatLayout):
    edge_detect = ObjectProperty()
        
class ButtonsLayout(RelativeLayout):
    normal = StringProperty()
    down = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.normal = 'icons/camera_white.png'
        self.down   = 'icons/camera_red.png'

        self.event = None
    def on_size(self, layout, size):

        self.ids.screen.min_state_time = 0.3 
        if Window.width < Window.height:
            self.pos = (0 , 0)
            self.size_hint = (1 , 0.2)
            self.ids.other.pos_hint  = {'center_x':.3,'center_y':.5}
            self.ids.other.size_hint = (.2, None)
            self.ids.screen.pos_hint  = {'center_x':.7,'center_y':.5}
            self.ids.screen.size_hint = (.2, None)
            self.ids.coin_plus.pos_hint  = {'center_x':.9,'center_y':.5}
            self.ids.coin_plus.size_hint = (.1, None)
            self.ids.coin_minus.pos_hint  = {'center_x':.1,'center_y':.5}
            self.ids.coin_minus.size_hint = (.1, None)
        else:
            self.pos = (Window.width * 0.8, 0)
            self.size_hint = (0.2 , 1)
            self.ids.other.pos_hint  = {'center_x':.5,'center_y':.3}
            self.ids.other.size_hint = (None, .2)
            self.ids.screen.pos_hint  = {'center_x':.5,'center_y':.7}
            self.ids.screen.size_hint = (None, .2)
            self.ids.coin_plus.pos_hint  = {'center_x':.5,'center_y':.9}
            self.ids.coin_plus.size_hint = (None, .1)
            self.ids.coin_minus.pos_hint  = {'center_x':.5,'center_y':.1}
            self.ids.coin_minus.size_hint = (None, .1)
    
    def take_photo(self, *args):
        try:
            token = store.get('user_data')['token']
        except Exception as e:
            response = requests.get('http://185.194.141.183:5002/api/get_token')
            token = response.json()["token"]
            store.put('user_data', token=token)
        self.parent.edge_detect.capture_screenshot()
        query = json.dumps(self.parent.edge_detect.model.last_result)
        query = query.encode('ascii')
        query = base64.b64encode(query).decode('ascii')
        webbrowser.open(f"http://185.194.141.183:5002/add?q={query}&token={token}")

    def scan_qr(self):
        try:
            token = store.get('user_data')['token']
        except Exception as e:
            response = requests.get('http://185.194.141.183:5002/api/get_token')
            token = response.json()["token"]
            store.put('user_data', token=token)
        try:
            self.parent.edge_detect.capture_photo(name="qr")
        except Exception as e:
            show_popup(str(e))

    def coin_reduce(self):
        self.parent.edge_detect.model.coin_reduce()
        
    def coin_increase(self):
        self.parent.edge_detect.model.coin_increase()

    def select_camera(self, facing):
        self.parent.edge_detect.select_camera(facing)


Builder.load_string("""
<AppLayout>:
    edge_detect: self.ids.preview
    EdgeDetect:
        aspect_ratio: '16:9'
        id:preview
    ButtonsLayout:
        id:buttons
<ButtonsLayout>:
    normal:
    down:
    Button:
        id:other
        on_press: root.scan_qr()
        height: self.width
        width: self.height
        background_normal: 'icons/qr-white.png'
        background_down:   'icons/qr-red.png'
    Button:
        id:screen
        on_press: root.take_photo()
        height: self.width
        width: self.height
        background_normal: root.normal
        background_down: root.down
    Button:
        id:coin_minus
        on_press: root.coin_reduce()
        height: self.width
        width: self.height
        background_normal: 'icons/minus-icon.png'
        background_down: 'icons/minus-icon.png'
    Button:
        id:coin_plus
        on_press: root.coin_increase()
        height: self.width
        width: self.height
        background_normal: 'icons/plus-icon.png'
        background_down: 'icons/plus-icon.png'
""")

            
