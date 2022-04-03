from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown

import sys
sys.path.append(".")


import subprocess

Builder.load_file('giu.kv')
messages_to_send = ["War is comming!", "", "fallus"]
latestID = -1


class OgWARning(App):
    def advertise_message(self, instance):
        message = messages_to_send.index(instance.text)
        priority = 999
        # time_stamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M')
        # time_stamp = hex(int(time_stamp))
        subprocess.call(f"sudo python3 ./advertise_ble.py -d {priority}{message}", shell=True)

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        self.window.add_widget(Image(source="2022_04_03_02u_Kleki.png"))

        self.dropdown = DropDown()
        for text in messages_to_send:
            btn = Button(text=text, size_hint_y=None, background_color=(1, 1, 1), background_normal="", height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text), on_press=self.advertise_message)
            self.dropdown.add_widget(btn)
        self.send_messages_button = Button(
            text='Send messages',
            size_hint=(1, 0.5),
            bold=True,
            background_color=(1, 1, 1),
            background_normal=""
        )
        self.send_messages_button.bind(on_release=self.dropdown.open)
        self.window.add_widget(self.send_messages_button)

        self.gotten_messages = Label(
            text='dupa cipa chuuuuuuuuuuuuUUuuj',
            font_size=18,
        )

        self.window.add_widget(self.gotten_messages)

        return self.window



if __name__ == "__main__":
    OgWARning().run()
