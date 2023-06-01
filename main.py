import sys, asyncio, os, json
from PySide6 import QtWidgets, QtCore

from comms import requests
from watcher import watcher
from m_utils import log as logging
from app_interface.window import Window

class ShapeShift:
    def __init__(self, config_fp):
        # create loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Plugin Config, used to prepop data
        self.config_fp = config_fp
        if os.path.isfile(self.config_fp):
            with open(config_fp) as file_handler:
                try:
                    self.config_json_dict = json.loads(file_handler.read())
                except Exception as e:
                    print(e)
        # Maybe TODO, split out config and only pass necessary data rather than the whole thing, probably not tho

        # VTS Connection
        self.vts_client = requests.VT_Requests(config_data=self.config_json_dict, new_model_handler=self.handle_new_models)
        # Watcher
        self.observer = watcher.Watcher(config_data=self.config_json_dict, event_handler=self.process_watcher_update)
        # GUI
        self.app = QtWidgets.QApplication(sys.argv)
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
        self.window.browse_button.clicked.connect(self.debug)
        self.window.set_watcher_status(self.observer.is_enabled)
        # remaining gui
        self.window.save_pref_button.clicked.connect(self.save_preferences)
        self.window.set_prefs_checkboxes(
            self.config_json_dict["plugin_settings"]["reload_model_on_fail"],
            self.config_json_dict["plugin_settings"]["update_data_on_new_model"],
            self.config_json_dict["plugin_settings"]["backup_folders"],
            self.config_json_dict["plugin_settings"]["start_watcher_on_startup"]
        )

    def kill_threads(self):
        self.observer.kill_thread()
        self.vts_client.kill_thread()

    def begin(self):
        self.window.show()
        if self.config_json_dict["cached_auth_token"]:
            self.connect_vts_ws()
        if self.config_json_dict["plugin_settings"]["start_watcher_on_startup"]:
            self.trigger_watcher()
        self.app.exec()

    def connect_vts_ws(self):
        self.loop.run_until_complete(self.vts_client.authenticate())
        self.window.set_plugin_status(self.vts_client.connected)
        self.config_json_dict["cached_auth_token"] = self.vts_client.auth_token
        self.save_prefs_tofile()

    def trigger_watcher(self):
        if self.observer.is_enabled:
            self.observer.disable_watcher()
        else:
            self.observer.enable_watcher()
        self.window.set_watcher_status(self.observer.is_enabled)

    # region remaining Slots
    def browse_button(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self.window, "Open Model Directory", "")
        self.config_json_dict["plugin_settings"]["model_directory"] = dir_path
        self.window.set_watcher_dir_input(dir_path)
        self.save_prefs_tofile()

    def save_preferences(self, save_model_dir = False):
        if save_model_dir:
            self.config_json_dict["plugin_settings"]["model_directory"] = self.window.directory_input.text()
        self.config_json_dict["plugin_settings"]["ws_base_url"] = self.window.url_input.text()
        self.config_json_dict["plugin_settings"]["ws_port"] = self.window.port_input.text()
        self.config_json_dict["plugin_settings"]["reload_model_on_fail"] = self.window.model_reload_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["update_data_on_new_model"] = self.window.update_data_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["backup_folders"] = self.window.backup_checkbox.isChecked()
        self.config_json_dict["plugin_settings"]["start_watcher_on_startup"] = self.window.run_watcher_checkbox.isChecked()
        self.save_prefs_tofile()

    # endregion

    # TODO rewrite as async
    def save_prefs_tofile(self):
        with open(self.config_fp, "w") as file_handler:
            try:
                file_handler.write(json.dumps(self.config_json_dict))
            except Exception as e:
                    print(e)

    def debug(self):
        asyncio.run(self.vts_client.reload_current_model())
        print("debug model reload")

    def process_watcher_update(self, event):
        """
        TODO
        job is to detect new changes from watcher.
        - validate requests and send to ws requests
            - check if vts connection is still valid, reconnect plugin if thats not the case
            - update ui for current plugin status (in cases where reload model isn't running despite the request)
        - cases of invalid might be verifying if watcher is looking at the correct dir (eg vts changed models, were not gonna set up events to listen for model changes since that really isn't the scope of this tool)
            - handle based on settings (update watcher or deactivate watcher)
        """
        self.loop.create_task(self.vts_client.reload_current_model())
        print("watcher event trig")
        # TODO use new_model_event to seamlessly update watcher look directory

    def handle_new_models(self):
        print("New Model Detected")
        pass

def ddb(event):
    print("on main event")


if __name__ == "__main__":
    app = ShapeShift("VTS-Shapeshift/debug/debug_config.json")
    app.begin()
    app.kill_threads()


    # config_fp = "VTS-Shapeshift/debug/debug_config.json"
    # if os.path.isfile(config_fp):
    #     with open(config_fp) as file_handler:
    #         try:
    #             print("zako")
    #             config_json_dict = json.loads(file_handler.read())
    #             mdir = "D:/SteamLibrary/steamapps/common/VTube Studio/VTube Studio_Data/StreamingAssets/Live2DModels"
    #             observer = watcher.Watcher(config_data=config_json_dict, event_handler=ddb)
    #             observer.enable_watcher()
    #         except Exception as e:
    #             print(e)

    # from watcher import test_wt
    # # wt = test_wt.Test_Watcher("D:/Projects/Big Mistake/watchdog tester")
    # # wt.enable_watcher()
    # wt = test_wt.Test_Watcher(dir="D:/Projects/Big Mistake/watchdog tester", event_handler=ddb)
    # wt.enable_watcher()

    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:

    #     print("keel")
    #     wt.kill_thread()
    pass

