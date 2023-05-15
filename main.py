
# Using Pyside to run our magic
import asyncio

from vtscomms import vts_requests
from watcher import watcher

if __name__ == "__main__":
    # TODO 
    print("== TODO update me==")
    vts_client = vts_requests.VTSRequests()
    model_dir = ("D:/Projects/Big Mistake/VTS-Shapeshift/test/testfiles/hiyori.2048")
    observer = watcher.Watcher(model_dir)

    #TODO rebuild async logic to call individual async methods inside vts_client, gonna be a doozy when implemented on PySide D:

