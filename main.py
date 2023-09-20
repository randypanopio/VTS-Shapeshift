import sys, asyncio, os, json, threading, string
from PySide6 import QtWidgets

from comms import requests
from watcher import watcher, backups
from m_utils import log as logging
from app_interface.window import Window

class ShapeShift:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.current_thread()
        self.thread.name = self.thread.name + " - ShapeShift_Thread"
        asyncio.set_event_loop(self.loop)

        self.set_configs()

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
        logging.ws_logger.info("killed all threads, exiting")

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
            logging.ws_logger.error("something went wrong with trying to connect, probably due to VTube Studio not being open")
            logging.ws_logger.error(e)
        sys.exit(self.app.exec())

    def connect_vts_ws(self):
        logging.ws_logger.info("Attempting to connect vts websocket")
        result = self.loop.run_until_complete(self.vts_client.authenticate())
        if result:
            self.config_json_dict["cached_auth_token"] = self.vts_client.auth_token
            self.save_prefs_tofile()
            logging.ws_logger.info("Saved Auth cache token")
        else:
            logging.ws_logger.info("Failed to connect vts websocket")
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

    def set_configs(self):
        # Plugin Config, used to prepop data
        self.config_fp = "plugin_config.json"
        if os.path.isfile(self.config_fp):
            with open(self.config_fp, "r") as file_handler:
                try:
                    self.config_json_dict = json.loads(file_handler.read())
                    logging.ws_logger.info("Existing config file found, populating plugin settings")
                except Exception as e:
                    logging.ws_logger.error(e)
        else:
            #TODO set file to readonly, and only writeable by this application
            logging.ws_logger.info("No config file found, creating new config file: "+self.config_fp)
            default_config = '{"plugin_config":{"apiName":"VTubeStudioPublicAPI","apiVersion":"1.0","pluginName":"VTS-Shapeshift","pluginDeveloper":"Roslin - Randy P"},"cached_auth_token":"","plugin_settings":{"connect_on_startup":false,"reload_model_on_fail":true,"update_data_on_new_model":true,"backup_folders":true,"restore_files_after_session":false,"start_watcher_on_startup":false,"model_directory":"","ws_base_url":"ws://localhost:","ws_port":"8001","wd_on_create":true,"wd_on_move":true,"wd_on_delete":true}}'
            with open(self.config_fp, "w+") as file_handler:
                try:
                    file_handler.write(default_config)
                except Exception as e:
                    logging.ws_logger.error(e)
            self.config_json_dict = json.loads(default_config)

        def log_bad_config(additional):
            logging.ws_logger.warning("Bad config settings! {0} contains bad settings, please delete {1} and restart the application".format(additional, self.config_fp))

        # Validate configs, set defaults
        if "plugin_config" not in self.config_json_dict:
            log_bad_config("plugin_config")
            self.config_json_dict["plugin_config"] = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "pluginName": "VTS-Shapeshift",
                "pluginDeveloper": "Roslin - Randy P"}

        if "cached_auth_token" not in self.config_json_dict:
            self.config_json_dict["cached_auth_token"]: string = ""

        if "plugin_settings" not in self.config_json_dict:
            log_bad_config("plugin_settings")
            self.config_json_dict["plugin_settings"] = {
                "connect_on_startup": True,
                "reload_model_on_fail": True,
                "update_data_on_new_model": True,
                "backup_folders": True,
                "restore_files_after_session": False,
                "start_watcher_on_startup": False,
                "model_directory": "",
                "ws_base_url": "ws://localhost:",
                "ws_port" : "8001",
                "wd_on_create" : True,
                "wd_on_move" : True,
                "wd_on_delete" : True
            }

    def save_prefs_tofile(self):
        with open(self.config_fp, "w") as file_handler:
            try:
                file_handler.write(json.dumps(self.config_json_dict))
                logging.ws_logger.info("prefs saved at: " + self.config_fp)
            except Exception as e:
                logging.ws_logger.error(e)

    def process_watcher_update(self, event):
        """
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
        logging.ws_logger.info("New model detected!")

if __name__ == "__main__":
    app = ShapeShift()
    app.open()