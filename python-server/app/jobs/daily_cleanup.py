import threading
import schedule
import time
from utils.folder_manager import FolderManager
import logging
import jobs_config
job_flag = True
from utils.custom_logger import CustomLogger
daily_cleanup_logger =  CustomLogger(log_file_path='app/logs/daily_cleanup.log', print_to_terminal=False, log_level=logging.DEBUG)
manager = FolderManager()
schedule.every(jobs_config.DELETE_DURATION_OF_DOWNLOADED_IMAGES).seconds.do(manager.clean_downloaded_images_folder)
daily_cleanup_logger.info("Started daily clean up of Downloaded Images")
def stop_job():
    global job_flag
    job_flag = False

def start_job():
    global job_flag
    job_flag = True

def job():
    print("I'm working...")

def scheduled_task():
    while job_flag:
        schedule.run_pending()
        time.sleep(1) # sleep until the time of job comes by two seconds
# Start the scheduled task in a separate thread
task_thread = threading.Thread(target=scheduled_task)
task_thread.daemon = True
task_thread.start()
