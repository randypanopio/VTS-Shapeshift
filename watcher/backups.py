import os, shutil, sys, time, string, threading, logging
from watchdog.observers import Observer
from m_utils import log as logging
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler


"""
    create a backup for current session. on new sess, check if backup exists, if not create backup
    if backup folder exists, compare if backup matches latest files, if not matching, create new backup?
"""
current_backup_dir_name = ".current_watcher_backup"
previous_session_backup_name = ".previous_watcher_backup"

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

#confgi settings - reset_post_session