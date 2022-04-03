import asyncio

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown

from threading import Thread
from multiprocessing import Process

import sys
sys.path.append(".")


import subprocess

Builder.load_file('giu.kv')
messages_to_send = ["War is comming!", "", "fallus"]
latestID = 0

global_label = Label(text="chuj")

class OgWARning(App):
    def advertise_message(self, instance):
        global latestID
        message = messages_to_send.index(instance.text)
        # time_stamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M')
        # time_stamp = hex(int(time_stamp))
        latestID += 1
        subprocess.call(f"sudo python3 ./advertise_ble.py -d {'0' * (3 - len(str(latestID))) + str(latestID)}{message}", shell=True)

    def read_message(self, instance):
        global latestID
        global global_label

        print("read message")
        with open("plik.txt", "r") as file:
            line = file.read()
            latestID = int(line[:3])
            global_label.text = line[3:]

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

        self.refresh_button = Button(
            text = "refresh messages",
            size_hint = (1, 0.5),
            background_color = (1, 1, 1),
            background_normal = ""
        )
        self.refresh_button.bind(on_release=self.read_message)
        self.window.add_widget(self.refresh_button)
        self.gotten_messages = global_label

        self.window.add_widget(self.gotten_messages)

        return self.window

def show_messgae(command):
    global_label.text = command

def run_scanner():
    print("run scannner")
    subprocess.call("python3 scanner.py", shell=True)



if __name__ == "__main__":
    OgWARning().run()

    # warning = OgWARning()
    #
    # proc1 = Thread(target=warning.run)
    # proc2 = Thread(target=run_scanner)
    # proc3 = Thread(target=read_message)
    #
    # proc1.run()
    # proc2.run()
    # proc3.run()
    #
    # proc1.join()
    # proc2.join()
    # proc3.join()
