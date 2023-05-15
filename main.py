
# Using Pyside to run our magic
import asyncio

import watcher
from vtscomms import requests
# w = watcher.Watcher()
# w.create_backup()
# w.watch("D:/Projects/Big Mistake/VTS-Shapeshift/test/testfiles/hiyori.2048")

cms = requests.VTSRequests()
# asyncio.run(cms.test())


async def testrun():
    from vtscomms import comms
    talk = comms.VTSRequests()
    await(talk.check_status())
    await(talk.authenticate())
    await(talk.check_status())    

if __name__ == "__main__":
    asyncio.run(testrun())
