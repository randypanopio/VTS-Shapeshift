
# Using Pyside to run our magic
import asyncio

import watcher
from vtscomms import requests
# w = watcher.Watcher()
# w.create_backup()
# w.watch("D:/Projects/Big Mistake/VTS-Shapeshift/test/testfiles/hiyori.2048")

cms = requests.VTSRequests()
# asyncio.run(cms.test())
cms.test()