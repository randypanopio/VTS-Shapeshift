from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon
import sys
from m_utils import links
# from m_utils import log as logging
from app_interface.widget import Ui_Form

class Window(QWidget, Ui_Form):
    _online_color = "green"
    _offline_color = "red"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("VTS-Shapeshift Plugin Application")
        self.setWindowIcon(QIcon("VTS-Shapeshift/files/images/icon.png"))
        self.twitter_button.clicked.connect(self.twitter_link)
        self.github_button.clicked.connect(self.github_link)

    def set_url_inputs(self, base_url = "", port = ""):
        self.url_input.setText(base_url)
        self.port_input.setText(port)

    def set_plugin_status(self, connected):
        self.plugin_status_label.setText("Connected" if connected else "Offline")
        self.plugin_status_label.setStyleSheet(
            "color: "+ Window._online_color +";"
            if connected else
            "color: "+ Window._offline_color +";"
        )

    def set_watcher_status(self, enabled):
        self.watcher_status_label.setText("Watching..." if enabled else "Disabled")
        self.watcher_status_label.setStyleSheet(
            "color: "+ Window._online_color +";"
            if enabled else
            "color: "+ Window._offline_color +";"
        )
        self.directory_input.setEnabled(not enabled)

    def set_watcher_dir_input(self, text = ""):
        self.directory_input.setText(text)

    def set_prefs_checkboxes(self, model_reload, update_data, backup):
        self.model_reload_checkbox.setChecked(model_reload)
        self.update_data_checkbox.setChecked(update_data)
        self.backup_checkbox.setChecked(backup)

    def twitter_link(self):
        links.open_url_browser("https://twitter.com/randypanopio")

    def github_link(self):
        links.open_url_browser("https://github.com/randypanopio/VTS-Shapeshift")