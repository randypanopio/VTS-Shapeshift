"""
    Objectives:
    Watchdog a file (performance first)
        - shouldn't be comparing and reading the whole file, could do dirty by date changes, or use watchdog 

    Trigger 

"""

import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def watch():
    dr = os.path.abspath("D:/Projects/Big Mistake/VTS-Shapeshift/test/testfiles/hiyori.2048/")
    fp = os.path.join(dr, "main.png")
    print("file path: "+ fp)
    # Set the format for logging info
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
 
    # Set format for displaying path
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
 
    # Initialize logging event handler
    event_handler = LoggingEventHandler()
 
    # Initialize Observer
    observer = Observer()
    observer.schedule(event_handler, dr, recursive=True)
 
    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()  