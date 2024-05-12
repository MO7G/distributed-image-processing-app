import subprocess
import os
import json

class CommandRunner:
    def __init__(self, file_path):
        self.file_path = file_path

    def run_mpi_command(self, args):
        directory = os.path.dirname(self.file_path)
        command = ["mpirun" ,"-np" , "4", os.path.join(directory, "filter.py")] + args
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error = process.communicate()

        output_str = output.decode()

        complex_obj = json.loads(output_str)

        if error:
            print("Error:", error.decode())

        return complex_obj
    
    def run_filter(self,args):
        final_directory = os.path.join(self.file_path , "filter.py")
        print(final_directory)
        command = ["mpirun" ,"-np" , "2" , "python" , final_directory]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        print("yes done")


# Example usage
if __name__ == "__main__":
    current_file_path = os.path.abspath(__file__)
    runner = CommandRunner("/home/mohd/Desktop/sharedFolder")
    x = runner.run_filter(["hello"])

