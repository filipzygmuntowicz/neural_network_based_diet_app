
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.lang import Builder


popup_kv = """
<P>:
    TextInput:
        multiline: True
        id:poplabel
        size_hint: 0.6, 0.2
        pos_hint: {"x": 0.2, "top":1}
"""
def show_popup(text):
    show = P()
    show.set_text(text)
    popupWindow = Popup(title="test", content=show, size_hint=(None, None), size=(800,800))
    popupWindow.open()

class P(FloatLayout):
    def __init__(self, **args):
        Builder.load_string(popup_kv)
        super().__init__(**args)
    def set_text(self, text):
        self.ids.poplabel.text = text
