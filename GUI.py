from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class OgWARning(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        self.send_messages_button = Button(
            text='Send messages',
            size_hint=(1, 0.5),
            bold=True,
            background_color='#00FFCE'
        )
        self.window.add_widget(self.send_messages_button)

        self.gotten_messages = Label(
            text='dupa cipa chuuuuuuuuuuuuUUuuj',
            font_size=18,
            color='#e6ffee'
        )

        self.window.add_widget(self.gotten_messages)

        return self.window






if __name__ == "__main__":
    OgWARning().run()
