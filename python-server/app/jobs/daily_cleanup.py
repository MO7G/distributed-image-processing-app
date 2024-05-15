import threading
import schedule
import time
from utils.folder_manager import FolderManager
import jobs_config

job_flag = True

manager = FolderManager()
schedule.every(jobs_config.DELETE_DURATION_OF_DOWNLOADED_IMAGES).seconds.do(manager.clean_downloaded_images_folder)

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
        time.sleep(1)

# Start the scheduled task in a separate thread
task_thread = threading.Thread(target=scheduled_task)
task_thread.daemon = True
task_thread.start()
