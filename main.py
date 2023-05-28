
# Using Pyside to run our magic
import sys, asyncio, os, json
from PySide6 import QtWidgets

from comms import requests
from watcher import watcher
from m_utils import log as logging
from app_interface.window import Window

class ShapeShift:
    def __init__(self):
        # VTS Connection
        self.vts_client = None #requests.VT_Requests(True, new_model_handler=handle_new_models)

        # GUI
        self.app = QtWidgets.QApplication(sys.argv)        
        self.window = Window()
        self.window.connection_button.clicked.connect(self.connect_button)
        pass

    # TODO grab cahced url from plugin config, also it should be reflected from settings
    def connect_button(self):
        if self.vts_client is None:
            self.vts_client = requests.VT_Requests(True, new_model_handler=handle_new_models)
        else:
            asyncio.run(self.vts_client.authenticate())

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



def test(event):
    print("i am a watcher in main, call the reload function")
    print("event: " + str(event))

def randprint():
    print("rand print")

# TODO
def handle_new_models():
    pass


    pass

#TODO prefill from plugin config







# # Watcher
# cached_dir = "CACHED_PATH" #Prefill from plugin config cache
# observer = watcher.Watcher(dir=cached_dir, event_handler=process_watcher_update)
# if os.path.exists(cached_dir):
#     observer.watch()
# else:
#     #TODO disable gui
#     pass




if __name__ == "__main__":
    s = ShapeShift()
    s.open_window()

    

    # vts_client = vts_requests.VT_Requests(True, new_model_handler=handle_new_models)
    # model_data = asyncio.run(vts_client.get_current_model_data())
    # print("JISDBGKJ\n"+json.dumps(model_data))
    # print("current model id: " + vts_client.model_id)
    # model_dir = ("D:/SteamLibrary/steamapps/common/VTube Studio/VTube Studio_Data/StreamingAssets/Live2DModels/hiyori_test")
    # observer = watcher.Watcher(model_dir, event_handler=test)
    # observer.watch()


    #TODO rebuild async logic to call individual async methods inside vts_client, gonna be a doozy when implemented on PySide D:

    pass

"""
on launch:
 - check if there is a previous session. update gui for fast enable


"""