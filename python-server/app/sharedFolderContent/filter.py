from mpi4py import MPI
import cv2
import threading
import queue
import time
from folder_navigator import FolderNavigator
path_to_DownloadedImages = "/home/mohd/Desktop/sharedFolder/DownloadedImages/"

class WorkerThread(threading.Thread):
    def __init__(self, task_queue,folder_name,rank=0):
        super().__init__()
        self.task_queue = task_queue
        self.rank = rank
        self.folder_name = folder_name
        self.dist_folder = "/home/mohd/Desktop/sharedFolder/DownloadedImages/" + folder_name + "/";
    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                #print(f"Rank {self.rank}, Thread {self.name} is done.")
                break  # Exit the loop if termination signal is received
            # Unpack the task
            image, operation = task
            # Process the image
            result = self.process_image(image, operation)
            #print(f"Thread {self.name} done processing {image} with {operation}.")
            # Add the result to the result queue

            image_path = self.dist_folder + "result" + "/" + image + '.png';
            print("this is hte image path  " , image_path);
            cv2.imwrite(image_path,result);


    def process_image(self, image, operation):
        path = self.dist_folder + image; 
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if operation == 'edge_detection':
            result = cv2.Canny(img, 100, 200)
        elif operation == 'color_inversion':
            result = cv2.bitwise_not(img)
        elif operation == 'increase_brightness':
            result = self.increase_brightness(img)
        # Add more operations as needed...
        return result

    def increase_brightness(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v += 50
        final_hsv = cv2.merge((h, s, v))
        result = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return result





def main(task_queue,folder_name):
    start_time = time.time()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    print(task_queue);
    # in case one process is running only then we are going to process locally here in the master node
    if size == 1:
        # Create a task queue and a result queue
        local_task_queue = queue.Queue()
        local_result_queue = queue.Queue()
        # Create and start worker threads
        while not task_queue.empty():
            temp = task_queue.get();
            local_task_queue.put(temp);
            


        local_num_threads = 2;

        for _ in range(local_num_threads):
            local_task_queue.put(None)

        threads = []
        for _ in range(local_num_threads):
            thread = WorkerThread(local_task_queue , folder_name)
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()


        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time  # Calculate the execution time
        #print(f"Execution time: {execution_time} seconds helloe")




    else:
        if rank == 0:
            # Master node
            task_queue_size = task_queue.qsize()
            tasks_per_process = task_queue_size // (size - 1)
            remainder = task_queue_size % (size - 1)

            start_index = 0
            for dest in range(1, size):
                if dest <= remainder:
                    num_of_task_for_current_process = tasks_per_process + 1;
                else:
                    num_of_task_for_current_process = tasks_per_process;

                end_index = start_index + num_of_task_for_current_process;
                subtasks = task_queue[start_index:end_index]
                #print(f"Sending tasks {subtasks} to worker node {dest}")
                MPI.COMM_WORLD.send(subtasks, dest=dest)
                start_index = end_index

            # Receive and handle results from worker nodes
            results = []
            for _ in range(size - 1):
                received_data = MPI.COMM_WORLD.recv(source=MPI.ANY_SOURCE)
                if isinstance(received_data, list):
                    # If received data is a list, assume it contains multiple images
                    results.extend(received_data)
                else:
                    # If received data is not a list, assume it's a single image
                    results.append(received_data)


            end_time = time.time()  # Record the end time
            execution_time = end_time - start_time  # Calculate the execution time
            #print(f"Execution time: {execution_time} seconds helloe")


        else:
            # Worker nodes
            #print(f"Rank {rank} entered the worker node block.")
            # Create a task queue and a result queue
            task_queue = queue.Queue()

            # Create and start worker threads
            num_threads = 1  # Example: Adjust the number of threads as needed
            # Listen for tasks from the master node
            tasks = MPI.COMM_WORLD.recv(source=0)
            #print(f"Rank {rank} received task: {tasks}")
            # Add the task to the task queue
            for task in tasks:
                task_queue.put(task)

            for _ in range(num_threads):
                task_queue.put(None)

            threads = []
            for _ in range(num_threads):
                thread = WorkerThread(task_queue, folder_name, rank)
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()


            # Send the list of results back to the master node
            MPI.COMM_WORLD.send(True, dest=0)



if __name__ == "__main__":
    folder_name = "913afd92-dd7c-4b42-8139-9a85f93333ce"
    operation = "color_inversion"
    folder_nav = FolderNavigator();
    list_of_images = folder_nav.list_files_in_folder(folder_name)
    task_queue = queue.Queue();
    for image_name in list_of_images:
        task_queue.put((image_name, operation))

    main(task_queue , folder_name)