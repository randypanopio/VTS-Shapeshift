
# Using Pyside to run our magic
import sys, asyncio, os, json
from PySide6 import QtWidgets

from comms import requests
from watcher import watcher
from m_utils import log as logging
from app_interface.window import Window

def test(event):
    print("i am a watcher in main, call the reload function")
    print("event: " + str(event))

def randprint():
    print("rand print")

# TODO
def handle_new_models():
    pass

def process_watcher_update():
    """
    my job is to detect new changes from watcher. 
    - validate requests and send to ws requests
        - check if vts connection is still valid, reconnect plugin if thats not the case
        - update ui for current plugin status (in cases where reload model isn't running despite the request)
    - cases of invalid might be verifying if watcher is looking at the correct dir (eg vts changed models, were not gonna set up events to listen for model changes since that really isn't the scope of this tool)
        - handle based on settings (update watcher or deactivate watcher)
    """
    asyncio.run(vts_client.reload_current_model())
    # TODO use new_model_event to seamlessly update watcher look directory
    pass

#TODO prefill from plugin config





# VTS Connection
vts_client = None #requests.VT_Requests(True, new_model_handler=handle_new_models)

# Watcher
cached_dir = "CACHED_PATH" #Prefill from plugin config cache
observer = watcher.Watcher(dir=cached_dir, event_handler=process_watcher_update)
if os.path.exists(cached_dir):
    observer.watch()
else:
    #TODO disable gui
    pass

# TODO grab cahced url from plugin config, also it should be reflected from settings
def connect_button():
    if vts_client is None:
        vts_client = requests.VT_Requests(True, new_model_handler=handle_new_models)
    asyncio.run(vts_client.authenticate())
    
    pass



if __name__ == "__main__":
    # GUI
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    window.connection_button.clicked.connect(connect_button)
    window.set_watcher_button_interactive(False)
    app.exec()    

    

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