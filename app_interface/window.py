from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon
import sys
from m_utils import links
from app_interface.widget import Ui_Form

class Window(QWidget, Ui_Form):
    ONLINE_COLOR = "rgb(39, 255, 118)"
    OFFLINE_COLOR = "rgb(255, 60, 0)"
    ONLINE_STYLE = "color: "+ ONLINE_COLOR +";"
    OFFLINE_STYLE =  "color: "+ OFFLINE_COLOR +";"

    BOLD_FSIZE = "font-size: 20px;"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("VTS-Shapeshift Plugin Application")
        self.setWindowIcon(QIcon("VTS-Shapeshift/files/images/icon.png"))
        self.twitter_button.clicked.connect(self.twitter_link)
        self.github_button.clicked.connect(self.github_link)
        self.watcher_secondary_label.setText("")

    def set_url_inputs(self, base_url = "", port = ""):
        self.url_input.setText(base_url)
        self.port_input.setText(port)

    def set_plugin_status(self, connected):
        self.plugin_status_label.setText("Connected" if connected else "Offline")
        clr  = Window.ONLINE_STYLE if connected else Window.OFFLINE_STYLE
        self.plugin_status_label.setStyleSheet(clr + Window.BOLD_FSIZE)

    def set_watcher_status(self, enabled):
        if enabled:
            self.watcher_status_label.setText("Watching...")
            self.watcher_button.setText("Disable")
            self.watcher_status_label.setStyleSheet(Window.BOLD_FSIZE + Window.ONLINE_STYLE)
            self.directory_input.setEnabled(False)
            self.browse_button.setEnabled(False)
        else:
            self.watcher_status_label.setText("Disabled")
            self.watcher_button.setText("Enable")
            self.watcher_status_label.setStyleSheet(Window.BOLD_FSIZE + Window.OFFLINE_STYLE)
            self.directory_input.setEnabled(True)
            self.browse_button.setEnabled(True)

    def set_watcher_dir_input(self, text = ""):
        self.directory_input.setText(text)

    def twitter_link(self):
        links.open_url_browser("https://twitter.com/randypanopio")

    def github_link(self):
        links.open_url_browser("https://github.com/randypanopio/VTS-Shapeshift")


"""
TODO add these tooltips:

backup:
Creates a copy of the model folder, and can be used to revert after session, or just for sanity sake. Creates the backup when the watcher is first enabled.

restore:
Restores the model folder to the original files after the application has been closed. Requires the backup setting to be enabled. If the backup folder is deleted for any reason, shapeshift will keep the existing folder structure alone.
"""