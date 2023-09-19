import sys, asyncio, os, json, threading, time
from PySide6 import QtWidgets, QtCore

from comms import requests
from watcher import watcher, backups
from m_utils import log as logging
from app_interface.window import Window

class ShapeShift:
    def __init__(self, config_fp):
        # Threading
        self.loop = asyncio.new_event_loop()
        self.thread = threading.current_thread()
        self.thread.name = self.thread.name + " - ShapeShift_Thread"
        asyncio.set_event_loop(self.loop)

        # Plugin Config, used to prepop data
        self.config_fp = config_fp
        if os.path.isfile(self.config_fp):
            with open(config_fp) as file_handler:
                try:
                    # TODO config file might be an easy way to debug. add a default config generator when the file has been deleted
                    self.config_json_dict = json.loads(file_handler.read())
                except Exception as e:
                    print(e)
        # Maybe TODO, split out config and only pass necessary data rather than the whole thing, probably won't because while the actual settings might be obfuscated within the code, it should remain relatively small, and generally be used across all the application

        # VTS Connection
        self.vts_client = requests.VT_Requests(config_data=self.config_json_dict, new_model_handler=self.handle_new_models)

        # Watcher
        self.observer = watcher.Watcher(
            config_data = self.config_json_dict,
            event_handler = self.process_watcher_update,
            trigger_on_create = self.config_json_dict["plugin_settings"]["wd_on_create"],
            trigger_on_move = self.config_json_dict["plugin_settings"]["wd_on_move"],
            trigger_on_delete = self.config_json_dict["plugin_settings"]["wd_on_delete"]
        )

        # Backup
        self.has_backed_up = False
        self.backup_dir = ""

        # Qt/GUI
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.aboutToQuit.connect(self.exit_application)
        self.window = Window()

        # vts requests gui
        self.window.connection_button.clicked.connect(self.connect_vts_ws)
        self.window.set_url_inputs(
            self.config_json_dict["plugin_settings"]["ws_base_url"],
            self.config_json_dict["plugin_settings"]["ws_port"]
        )
        self.window.set_plugin_status(self.vts_client.connected)
        # watcher gui
        self.window.watcher_button.clicked.connect(self.trigger_watcher)
        self.window.set_watcher_dir_input(self.config_json_dict["plugin_settings"]["model_directory"])
        self.window.browse_button.clicked.connect(self.browse_button)
        self.window.set_watcher_status(self.observer.is_enabled)
        # remaining gui
        self.window.save_pref_button.clicked.connect(self.save_preferences)
        self.window.model_reload_checkbox.setChecked(self.config_json_dict["plugin_settings"]["reload_model_on_fail"])
        self.window.update_data_checkbox.setChecked(self.config_json_dict["plugin_settings"]["update_data_on_new_model"])
        self.window.backup_checkbox.setChecked(self.config_json_dict["plugin_settings"]["backup_folders"])
        self.window.backup_checkbox.stateChanged.connect(self.backup_box)
        self.window.restore_file_checkbox.setChecked(self.config_json_dict["plugin_settings"]["restore_files_after_session"])
        self.window.run_watcher_checkbox.setChecked(self.config_json_dict["plugin_settings"]["start_watcher_on_startup"])
        self.window.startup_connect_checkbox.setChecked(self.config_json_dict["plugin_settings"]["connect_on_startup"])
        self.window.wd_on_create_checkbox.setChecked(self.config_json_dict["plugin_settings"]["wd_on_create"])
        self.window.wd_on_move_checkbox.setChecked(self.config_json_dict["plugin_settings"]["wd_on_move"])
        self.window.wd_on_delete_checkbox.setChecked(self.config_json_dict["plugin_settings"]["wd_on_delete"])


    def exit_application(self):
        self.save_preferences(save_model_dir=True)
        self.observer.kill_thread()
        if self.config_json_dict["plugin_settings"]["restore_files_after_session"] and self.backup_dir:
            backups.restore_from_backup(
                backup = self.backup_dir,
                to_replace = self.config_json_dict["plugin_settings"]["model_directory"]
            )
        print("killed all threads, exiting")

    def open(self):
        self.window.show()
        try:
            self.loop.run_until_complete(self.vts_client.connect_websocket())
            if self.config_json_dict["cached_auth_token"]:
                self.connect_vts_ws()

            on_startup = self.config_json_dict["plugin_settings"]["start_watcher_on_startup"]
            mdir = self.config_json_dict["plugin_settings"]["model_directory"]
            if on_startup and mdir:
                self.trigger_watcher()
        except Exception as e:
            print("something went wrong with trying to connect, probably due to VTube Studio not being open")
            print(e)
        sys.exit(self.app.exec())

    def connect_vts_ws(self):
        result = self.loop.run_until_complete(self.vts_client.authenticate())
        if result:
            self.config_json_dict["cached_auth_token"] = self.vts_client.auth_token
            self.save_prefs_tofile()
        self.window.set_plugin_status(result)

    def trigger_watcher(self):
        if self.observer.is_enabled:
            self.observer.disable_watcher()
        else:
            dir_path = self.window.directory_input.text()
            if not self.observer.dir == dir_path:
                self.config_json_dict["plugin_settings"]["model_directory"] = dir_path
                self.observer.update_directory(dir_path)
            if not self.has_backed_up:
                if self.config_json_dict["plugin_settings"]["model_directory"]:
                    self.backup_dir = backups.create_backup(self.config_json_dict["plugin_settings"]["model_directory"])
                    self.has_backed_up = True
            self.observer.enable_watcher()
        self.window.set_watcher_status(self.observer.is_enabled)

    # region remaining Slots
    def browse_button(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self.window, "Open Model Directory", "")
        if dir_path:
            self.config_json_dict["plugin_settings"]["model_directory"] = dir_path
            self.window.set_watcher_dir_input(dir_path)
            self.observer.update_directory(dir_path)
            self.window.watcher_secondary_label.setText("")
            # Assume that setting a new model path is basically a new session, so its safe to do a fresh backup?
            # TODO debilitate this lol
            if self.config_json_dict["plugin_settings"]["backup_folders"]:
                backups.create_backup(dir_path)
            self.save_prefs_tofile()

    def save_preferences(self, save_model_dir = True):
        if save_model_dir:
            self.config_json_dict["plugin_settings"]["model_directory"] = self.window.directory_input.text()
        self.config_json_dict["plugin_settings"]["ws_base_url"] = self.window.url_input.text()
        self.config_json_dict["plugin_settings"]["ws_port"] = self.window.port_input.text()
        self.config_json_dict["plugin_settings"]["reload_model_on_fail"] = self.window.model_reload_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["update_data_on_new_model"] = self.window.update_data_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["backup_folders"] = self.window.backup_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["restore_files_after_session"] = self.window.restore_file_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["start_watcher_on_startup"] = self.window.run_watcher_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["connect_on_startup"] = self.window.startup_connect_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["wd_on_create"] = self.window.wd_on_create_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["wd_on_move"] = self.window.wd_on_move_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["wd_on_delete"] = self.window.wd_on_delete_checkbox.isChecked()
        self.save_prefs_tofile()

    def backup_box(self):
        self.window.restore_file_checkbox.setEnabled(self.window.backup_checkbox.isChecked())
    # endregion

    def save_prefs_tofile(self):
        with open(self.config_fp, "w") as file_handler:
            try:
                file_handler.write(json.dumps(self.config_json_dict))
                print("prefs saved at: " + self.config_fp)
            except Exception as e:
                    print(e)

    def process_watcher_update(self, event):
        """
        TODO
        job is to detect new changes from watcher.
        - validate requests and send to ws requests
            - check if vts connection is still valid, reconnect plugin if thats not the case
            - update ui for current plugin status (in cases where reload model isn't running despite the request)
        """
        if self.vts_client.connected:
            self.loop.run_until_complete(self.vts_client.reload_current_model())

    def handle_new_models(self):
        # for now disable watcher, maybe later feature is automatically swapping to the new models dir, actually take advantage of update_data_on_new_model. Maybe for V2
        self.window.watcher_secondary_label.setText("new model detected!")
        self.observer.disable_watcher()
        self.window.set_watcher_status(self.observer.is_enabled)

if __name__ == "__main__":
    app = ShapeShift("VTS-Shapeshift/files/plugin_config.json")
    app.open()