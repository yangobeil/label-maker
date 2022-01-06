import os
import shutil

from kivymd.app import MDApp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

DEFAULT_IMAGE = 'logo.png'


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass


class LabelMaker(Widget):
    input = ObjectProperty(None)
    output = ObjectProperty(None)
    new_label = ObjectProperty(None)
    image_path = StringProperty(DEFAULT_IMAGE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = None
        self.image_labels = {}
        self.checkbox_widgets = {}
        self.add_list_item_with_checkbox('delete')

    def add_list_item_with_checkbox(self, text):
        item = OneLineAvatarIconListItem(text=text)
        checkbox = LeftCheckbox(group='labels checkboxes')
        checkbox.label = text
        checkbox.bind(on_release=self.update_label)
        self.checkbox_widgets[text] = checkbox
        item.add_widget(checkbox)
        self.ids.labels_list.add_widget(item)

    def load(self):
        if os.path.isdir(self.input.text):
            self.index = 0
            self.images = [os.path.join(self.input.text, name) for name in os.listdir(self.input.text)]
            self.image_path = self.images[self.index]

    def refresh_checkboxes(self):
        if self.image_path in self.image_labels.keys():
            self.checkbox_widgets[self.image_labels[self.image_path]].active = True
        else:
            for widget in self.checkbox_widgets.values():
                widget.active = False

    def next(self):
        if self.index is not None:
            self.index = min(self.index + 1, len(self.images) - 1)
            self.image_path = self.images[self.index]
            self.refresh_checkboxes()

    def previous(self):
        if self.index is not None:
            self.index = max(self.index - 1, 0)
            self.image_path = self.images[self.index]
            self.refresh_checkboxes()

    def add_label(self):
        if self.new_label.text:
            self.add_list_item_with_checkbox(text=self.new_label.text)
            self.new_label.text = ''

    def update_label(self, check):
        if check.active:
            self.image_labels[self.image_path] = check.label
        else:
            self.image_labels.pop(self.image_path, None)

    def move(self):
        if self.output.text:
            try:
                for image_path, label in self.image_labels.items():
                    if label == 'delete':
                        os.remove(image_path)
                    else:
                        destination = os.path.join(self.output.text, label)
                        if not os.path.isdir(destination):
                            os.mkdir(destination)
                        shutil.move(image_path, destination)
                self.restart()
                self.refresh_checkboxes()
            except Exception as e:
                print(e)

    def restart(self):
        self.input.text = ''
        self.output.text = ''
        self.index = None
        self.image_labels = {}
        self.images = []
        self.image_path = DEFAULT_IMAGE



class MainApp(MDApp):
    def build(self):
        return LabelMaker()


if __name__ == '__main__':
    MainApp().run()