import os
import shutil

from kivymd.app import MDApp
from kivy.core.window import Window
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
        # checkbox to delete image is always there
        self.add_list_item_with_checkbox('delete')
        # configure keyboard
        self._setup_keyboard()

    def _setup_keyboard(self):
        """ Give app control of the keyboard to monitor the keys that are hit."""
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        """ Function to call when the keyboard is requested by another widget to let go of it."""
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """ Do something when a key is pressed on the keyboard. Go to next image or previous one depending on
            arrow that was hit."""
        if keycode[1] == 'right':
            self.next()
        elif keycode[1] == 'left':
            self.previous()

        return True

    def add_list_item_with_checkbox(self, text):
        """ Create list item widget with a radio button checkbox and the required text. The checkbox widget is added to
            the list of widgets for use later. The whole widget is added to the app."""
        item = OneLineAvatarIconListItem(text=text)
        checkbox = LeftCheckbox(group='labels checkboxes')
        checkbox.selected_color = (0,0,0,1)
        checkbox.label = text
        checkbox.bind(on_release=self.update_label)
        self.checkbox_widgets[text] = checkbox
        item.add_widget(checkbox)
        self.ids.labels_list.add_widget(item)

    def load(self):
        """ Takes input directory, loads the paths of all the images in the directory and displays the first image."""
        if os.path.isdir(self.input.text):
            self.index = 0
            self.images = [os.path.join(self.input.text, name) for name in os.listdir(self.input.text)]
            self.image_path = self.images[self.index]

    def refresh_checkboxes(self):
        """ If current displayed image has a saved label, activate the corresponding checkbox. If not, deactivate all
            the checkboxes."""
        if self.image_path in self.image_labels.keys():
            self.checkbox_widgets[self.image_labels[self.image_path]].active = True
        else:
            for widget in self.checkbox_widgets.values():
                widget.active = False

    def next(self):
        """ Display the next image in the list (if not at the end) and update activation of checkboxes."""
        if self.index is not None:
            if self.index + 1 > len(self.images) - 1:
                self.index = 0
            else:
                self.index += 1
            self.image_path = self.images[self.index]
            self.refresh_checkboxes()

    def previous(self):
        """ Display the previous image in the list (if not at the start) and update activation of checkboxes."""
        if self.index is not None:
            if self.index - 1 < 0:
                self.index = len(self.images) - 1
            else:
                self.index -= 1
            self.image_path = self.images[self.index]
            self.refresh_checkboxes()

    def add_label(self):
        """ Add a new checkbox widget for a label if a new one exists."""
        if self.new_label.text:
            self.add_list_item_with_checkbox(text=self.new_label.text)
            self.new_label.text = ''

    def update_label(self, check):
        """ Used when a checkbox is touched. If it is activated the new label is saved for the current image. If it
            is deactivated, the saved label is deleted."""
        if check.active:
            self.image_labels[self.image_path] = check.label
        else:
            self.image_labels.pop(self.image_path, None)

    def move(self):
        """ Move or delete all the images with a saved label. Create label directory if necessary and restart the app
            at the end."""
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
        """ Return all the variables to their initial values."""
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