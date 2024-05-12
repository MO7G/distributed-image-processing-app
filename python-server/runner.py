import subprocess


def run_bash_script():
    # Command to run the Bash script
    bash_command = "./test.sh"

    try:
        # Run the Bash script using subprocess
        subprocess.run(bash_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during script execution
        print("Error running Bash script:", e)

    while True:
        pass;

if __name__ == "__main__":
    run_bash_script()
