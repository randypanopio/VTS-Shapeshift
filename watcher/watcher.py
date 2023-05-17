import os, shutil, sys, time
from watchdog.observers import Observer
from log import ws_logger as logging
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler


class Watcher:
    """
        create a backup for current session. on new sess, check if backup exists, if not create backup
        if backup folder exists, compare if backup matches latest files, if not matching, create new backup?
    """
    current_backup_dir_name = ".current_watcher_backup"
    previous_session_backup_name = ".previous_watcher_backup"

    def __init__(self, dir, event_handler = None, check_intialize_handler = None):
        self.dir = os.path.abspath(dir)
        self.event_handler = event_handler
        self.check_intialize_handler = check_intialize_handler
        self.observer = None

    def create_backup(self):
        backup_dir = os.path.join(self.dir, self.current_backup_dir_name)

        if not os.path.exists(backup_dir):
            try:
                print("trying to creating backup of directory: " + self.dir)
                shutil.copytree(self.dir, backup_dir)
            except Exception as e:
                print("unable to create a backup of: " + self.dir)
                print(e)
        else:
            # TODO add condition for reverting after session. as well as if we are to update the backup at the end of session
            print("backup exists at: " + backup_dir)

    def watch(self, 
            polling_interval = 1, 
            on_delete = True, 
            on_move = True, 
            on_create = True):
        patterns = ["*"]
        print("BEGIN WOTCH")
        event_handler = PatternMatchingEventHandler(patterns, None, False, True)
        event_handler.on_modified = self.trigger_event
        if on_delete:
            event_handler.on_deleted = self.trigger_event
        if on_move:
            event_handler.on_moved = self.trigger_event
        if on_create:
            event_handler.on_created = self.trigger_event

        # Initialize Observer
        observer = Observer()
        self.observer - observer
        self.observer.schedule(event_handler, self.dir, recursive=True)
    
        # Start the observer
        self.observer.start()
        try:
            while True:
                # Set the thread sleep time
                time.sleep(polling_interval)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
        self.initialized_watch()

    def initialized_watch(self):
        print("Watcher initalized observer on dir: " + self.dir)
        if self.check_intialize_handler:
            self.check_intialize_handler()

    def trigger_event(self, event):
        if self.event_handler:
            self.event_handler(event)

    # TODO build me, OR implement initalizing new observer if it makes sense that way.
    # Likely updating observer's dir probably faster performance wise, gotta test 
    def update_directory(self, directory):
        pass
 