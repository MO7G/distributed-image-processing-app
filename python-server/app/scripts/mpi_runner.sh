#!/bin/bash

# Set the path to the Python script
PYTHON_SCRIPT="/home/mohd/Desktop/sharedFolder/filter.py"
HOSTS_CONFIG="/home/mohd/Desktop/sharedFolder/hosts.txt"
FOLDER_NAME="$1"
OPERATION="$2"

# Execute the MPI command with command-line arguments
mpirun --hostfile "$HOSTS_CONFIG"  --np 2 python "$PYTHON_SCRIPT" "$FOLDER_NAME" "$OPERATION"
