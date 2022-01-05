import os

from kivymd.app import MDApp
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.list import OneLineListItem
from kivy.uix.widget import Widget

DEFAULT_IMAGE = 'logo.png'


class LabelMaker(Widget):
    input = ObjectProperty(None)
    output = ObjectProperty(None)
    new_label = ObjectProperty(None)
    image_path = StringProperty(DEFAULT_IMAGE)
    index = None

    def load(self):
        if os.path.isdir(self.input.text):
            self.index = 0
            self.images = [os.path.join(self.input.text, name) for name in os.listdir(self.input.text)]
            self.image_path = self.images[self.index]

    def next(self):
        if self.index is not None:
            self.index = min(self.index + 1, len(self.images) - 1)
            self.image_path = self.images[self.index]

    def previous(self):
        if self.index is not None:
            self.index = max(self.index - 1, 0)
            self.image_path = self.images[self.index]

    def add_label(self):
        if self.new_label.text:
            self.ids.labels_list.add_widget(OneLineListItem(text=self.new_label.text))
            self.new_label.text = ''


class MainApp(MDApp):
    def build(self):
        return LabelMaker()


if __name__ == '__main__':
    MainApp().run()