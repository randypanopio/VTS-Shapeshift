import os, shutil
from pathlib import Path
from m_utils import log as logging

backup_affix = "_VTS_Shapeshift_Backup"

def create_backup(dir):
    backup_dir = dir + backup_affix
    if not os.path.exists(backup_dir):
        try:
            shutil.copytree(dir, backup_dir)
            logging.ws_logger.info("backup created at: " + backup_dir)
        except Exception as e:
            logging.ws_logger.error("unable to create a backup of: " + dir)
            logging.ws_logger.error(e)
    else:
        logging.ws_logger.info("removing existing backup at: " + backup_dir + "\ncreating a new backup for this session")
        shutil.rmtree(backup_dir)
        create_backup(dir)
    return backup_dir

def restore_from_backup(backup, to_replace):
    """
        this function will automatically delete the backup folder upon succeeding
    """
    backup = os.path.abspath(backup)
    to_replace = os.path.abspath(to_replace)
    source = Path(backup)
    target = Path(to_replace)

    if backup == to_replace:
        logging.ws_logger.info("Passed target and backup as the same path")
        return False

    if backup in target.parents:
        logging.ws_logger.info("Backup is contained within the passed target")
        # I mean we could handle this but nah
        return False

    # check if backup is in same root dir, can just delete target, rename backup
    if source.parents[0] == target.parents[0]:
        try:
            shutil.rmtree(to_replace)
            os.rename(backup, to_replace)
            return True
        except Exception as e:
            logging.ws_logger.error(e)
            return False
    else:
        try:
            shutil.rmtree(to_replace)
            shutil.copytree(backup, to_replace)
            shutil.rmtree(backup)
            return True
        except Exception as e:
            logging.ws_logger.error(e)
            return False
    return False