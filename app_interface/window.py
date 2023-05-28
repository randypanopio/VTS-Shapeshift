from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon
import sys
# from m_utils import log as logging
from app_interface.widget import Ui_Form

class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("VTS-Shapeshift Plugin Application")
        self.setWindowIcon(QIcon("VTS-Shapeshift/files/images/icon.png"))




    def set_plugin_status(self, text):
        self.plugin_status_label.text = text

    def set_watcher_status(self, text):
        self.watcher_status_label.text = text

    def set_watcher_button_label(self, text):
        self.watcher_status_label.text = text

    def set_watcher_button_interactive(self, enable = True):
        self.watcher_button.setEnabled(enable)
        if not enable:
            self.set_watcher_button_label("Invalid Directory!")
        # else: # updating label likely should be handled elsewhere when enabled again
        #     self.set_watcher_button_label("")