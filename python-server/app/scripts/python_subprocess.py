import os
import subprocess

def run_command_with_subprocess(folder_name,operation):
    """
    Run a command using subprocess and return the standard output and standard error.

    Returns:
    - stdout (str): Standard output of the command.
    - stderr (str): Standard error of the command.
    """
    # Get the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Construct the full path to mpi_runner.sh
    mpi_runner_path = os.path.join(current_directory, 'mpi_runner.sh')
    
    # Define the command
    command = [mpi_runner_path, folder_name, operation]
    
    # Run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the process to finish and get the output
    stdout, stderr = process.communicate()
    
    # Decode stdout and stderr
    stdout = stdout.decode()
    stderr = stderr.decode()
    
    # Print the output
    print("Standard Output:")
    print(stdout)
    print("\nStandard Error:")
    print(stderr)