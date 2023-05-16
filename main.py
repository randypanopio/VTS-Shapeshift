
# Using Pyside to run our magic
import asyncio

from vtscomms import vts_requests
from watcher import watcher

def test(event):
    print("i am a watcher in main, call the reload function")
    print("event: " + str(event))

if __name__ == "__main__":
    # TODO 
    print("== TODO update me==")
    vts_client = vts_requests.VTSRequests()
    asyncio.run(vts_client.authenticate())
    model_dir = ("D:/SteamLibrary/steamapps/common/VTube Studio/VTube Studio_Data/StreamingAssets/Live2DModels/hiyori_test")
    observer = watcher.Watcher(model_dir, event_handler=test)
    observer.watch()


    #TODO rebuild async logic to call individual async methods inside vts_client, gonna be a doozy when implemented on PySide D:

