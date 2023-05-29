import os, shutil, sys, time, string
from watchdog.observers import Observer
from m_utils import log as logging
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler


class Watcher:
    """
        create a backup for current session. on new sess, check if backup exists, if not create backup
        if backup folder exists, compare if backup matches latest files, if not matching, create new backup?
    """
    current_backup_dir_name = ".current_watcher_backup"
    previous_session_backup_name = ".previous_watcher_backup"

    def __init__(self, config_data, event_handler = None):
        if config_data["plugin_settings"]["model_directory"]:
            self.dir = os.path.abspath(config_data["plugin_settings"]["model_directory"])
        else:
            self.dir: string = ""
        self.event_handler = event_handler
        self.observer = Observer()
        self.enabled = False
        self.initialized = False

    def setup_watch(self, 
            polling_interval = 1, 
            on_delete = True, 
            on_move = True, 
            on_create = True):
        
        if not self.dir:
            print("Directory has not yet been set up")
            return
        
        patterns = ["*"]
        print("setup watch")
        event_handler = PatternMatchingEventHandler(patterns, None, False, True)
        event_handler.on_modified = self.trigger_event
        if on_delete:
            event_handler.on_deleted = self.trigger_event
        if on_move:
            event_handler.on_moved = self.trigger_event
        if on_create:
            event_handler.on_created = self.trigger_event
        self.observer.schedule(event_handler, self.dir, recursive=True)
        self.enabled = True
    

        # TODO create a separate thread to run watcher

        # Start the observer
        self.observer.start()
        self.enabled = True
        try:
            while True:
                # Set the thread sleep time
                time.sleep(polling_interval)
        except Exception as e:
            print(e)
        self.observer.join()
        self.initialized = True

    def trigger_event(self, event):
        if self.event_handler:
            self.event_handler(event)

    def enable_watcher(self):
        if self.enabled:
            pass
        else:
            if not self.initialized:
                self.setup_watch()
            else:
                self.observer.start()
                self.enabled = True
                print("enabled observer")

    def disable_watcher(self):
        if self.enabled is False:
            pass
        else:       
            self.observer.stop()
            self.enabled = False
            print("disabled observer")

    # TODO build me, OR implement initalizing new observer if it makes sense that way.
    # Likely updating observer's dir probably faster performance wise, gotta test 
    def update_directory(self, directory):
        pass
  
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
