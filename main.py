
# Using Pyside to run our magic
import asyncio, json

from comms import requests
from watcher import watcher

def test(event):
    print("i am a watcher in main, call the reload function")
    print("event: " + str(event))

def handle_new_models():
    pass

if __name__ == "__main__":
    # TODO 
    print("== TODO update me==")
    # vts_client = vts_requests.VT_Requests(True, new_model_handler=handle_new_models)
    # model_data = asyncio.run(vts_client.get_current_model_data())
    # print("JISDBGKJ\n"+json.dumps(model_data))
    # print("current model id: " + vts_client.model_id)
    # model_dir = ("D:/SteamLibrary/steamapps/common/VTube Studio/VTube Studio_Data/StreamingAssets/Live2DModels/hiyori_test")
    # observer = watcher.Watcher(model_dir, event_handler=test)
    # observer.watch()


    #TODO rebuild async logic to call individual async methods inside vts_client, gonna be a doozy when implemented on PySide D:


"""
on launch:
 - check if there is a previous session. update gui for fast enable


"""