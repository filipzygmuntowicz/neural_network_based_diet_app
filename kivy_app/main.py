from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from applayout import AppLayout, store
from android_permissions import AndroidPermissions
import os
import requests
import sys
from jnius import autoclass
from android.runnable import run_on_ui_thread
from android import mActivity
from popup import show_popup


View = autoclass('android.view.View')
@run_on_ui_thread
def hide_landscape_status_bar(instance, width, height):
    if Window.width > Window.height: 
        option = View.SYSTEM_UI_FLAG_FULLSCREEN
    else:
        option = View.SYSTEM_UI_FLAG_VISIBLE
    mActivity.getWindow().getDecorView().setSystemUiVisibility(option)


class MyApp(App):

    def build(self):
        self.layout = AppLayout()
        Window.bind(on_resize=hide_landscape_status_bar)
        return self.layout

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)
        
    def start_app(self):
        self.dont_gc = None
        Clock.schedule_once(self.connect_camera)

    def connect_camera(self,dt):
        self.layout.edge_detect.connect_camera(analyze_pixels_resolution = 720,
                                               enable_analyze_pixels = True,
                                               enable_video = False,
                                               default_zoom=0,
                                               filepath_callback=self.send_photo_to_webapp)
    def on_stop(self):
        self.layout.edge_detect.disconnect_camera()

    def send_photo_to_webapp(self, fpath):
        fpath = f"/storage/self/primary/{fpath}"
        if "qr" in fpath:
            data = {"token":store.get('user_data')['token']}
            files = {'qr': open(fpath, "rb")}
            response = requests.post('http://185.194.141.183:5002/api/qr', files=files, data=data)
            token = response.json()["token"]
            id = response.json()["id"]
            self.layout.edge_detect.connected_id = id
            store.put('user_data', token=token)
        else:
            data = {'token': store.get('user_data')['token']}
            files = {'products_image': open(fpath, "rb")}
            response = requests.post('http://185.194.141.183:5002/api/products_image', files=files, data=data)
        
        os.remove(fpath)
        

MyApp().run()
