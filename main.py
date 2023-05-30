import sys, asyncio, os, json
from PySide6 import QtWidgets

from comms import requests
from watcher import watcher
from m_utils import log as logging
from app_interface.window import Window

class ShapeShift:
    def __init__(self, config_fp):
        # Plugin Config, used to prepop data
        if os.path.isfile(config_fp):
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
        self.window.connection_button.clicked.connect(self.connect_button)
        self.window.plugin_status_label.setText("Connected" if self.vts_client.connected else "Offline")
        self.window.plugin_status_label.setStyleSheet("color: green;" if self.vts_client.connected else "color: red;")
        self.window.url_input.setText(self.config_json_dict["plugin_settings"]["ws_base_url"])
        self.window.port_input.setText(self.config_json_dict["plugin_settings"]["ws_port"])        

        # watcher gui
        self.window.watcher_button.clicked.connect(self.watcher_button)
        self.window.watcher_status_label.setText("Watching..." if self.observer.enabled else "Disabled")
        self.window.watcher_status_label.setStyleSheet("color: green;" if self.observer.enabled else "color: red;")
        self.window.directory_input.setEnabled(False if self.observer.enabled else True)
        self.window.directory_input.setText(self.config_json_dict["plugin_settings"]["model_directory"])
        self.window.browse_button.clicked.connect(self.browse_button)

        # remaining settings gui
        self.window.save_pref_button.clicked.connect(self.save_prefs_button)
        self.window.model_reload_checkbox.setChecked(self.config_json_dict["plugin_settings"]["reload_model_on_fail"])
        self.window.update_data_checkbox.setChecked(self.config_json_dict["plugin_settings"]["update_data_on_new_model"])
        self.window.backup_checkbox.setChecked(self.config_json_dict["plugin_settings"]["backup_folders"])



    # TODO grab cahced url from plugin config, also it should be reflected from settings
    # TODO ui still freezing despite running in a separate thread :(
    def connect_button(self):
        asyncio.run(self.vts_client.authenticate())
        self.window.plugin_status_label.setText("Connected" if self.vts_client.connected else "Offline")
        self.window.plugin_status_label.setStyleSheet("color: green;" if self.vts_client.connected else "color: red;")
            
    def watcher_button(self):
        """
        on start - do nothing
        check current status and process what to do next (eg toggle on or off)
        """
        status = self.observer.enabled
        if status:
            self.observer.disable_watcher()
        else:
            self.observer.enable_watcher() 
        # Sync UI. True value should only come from observer
        self.window.watcher_button.setText("Disable" if status else "Enable") # note, status was flipped from status above
        self.window.watcher_status_label.setText("Disabled" if status else "Watching...")
        self.window.watcher_status_label.setStyleSheet("color: red;" if status else "color: green;")
        self.window.directory_input.setEnabled(False if self.observer.enabled else True)

    def browse_button(self):
        pass

    def save_prefs_button(self):
        pass

    def process_watcher_update(self):
        """
        my job is to detect new changes from watcher. 
        - validate requests and send to ws requests
            - check if vts connection is still valid, reconnect plugin if thats not the case
            - update ui for current plugin status (in cases where reload model isn't running despite the request)
        - cases of invalid might be verifying if watcher is looking at the correct dir (eg vts changed models, were not gonna set up events to listen for model changes since that really isn't the scope of this tool)
            - handle based on settings (update watcher or deactivate watcher)
        """
        asyncio.run(self.vts_client.reload_current_model())
        # TODO use new_model_event to seamlessly update watcher look directory

    def open_window(self):
        self.window.show()
        self.app.exec()    

    def handle_new_models(self):
        pass


#TODO prefill from plugin config
if __name__ == "__main__":
    s = ShapeShift("VTS-Shapeshift/debug/debug_config.json")
    s.open_window()






# # Watcher
# cached_dir = "CACHED_PATH" #Prefill from plugin config cache
# observer = watcher.Watcher(dir=cached_dir, event_handler=process_watcher_update)
# if os.path.exists(cached_dir):
#     observer.watch()
# else:
#     #TODO disable gui
#     pass





    

    # vts_client = vts_requests.VT_Requests(True, new_model_handler=handle_new_models)
    # model_data = asyncio.run(vts_client.get_current_model_data())
    # print("JISDBGKJ\n"+json.dumps(model_data))
    # print("current model id: " + vts_client.model_id)
    # model_dir = ("D:/SteamLibrary/steamapps/common/VTube Studio/VTube Studio_Data/StreamingAssets/Live2DModels/hiyori_test")
    # observer = watcher.Watcher(model_dir, event_handler=test)
    # observer.watch()


    #TODO rebuild async logic to call individual async methods inside vts_client, gonna be a doozy when implemented on PySide D:
