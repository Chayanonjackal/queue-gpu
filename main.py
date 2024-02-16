import time
import GPUtil
import subprocess


def input_cli():
    cli = input('Input your cli...\n')
    return cli

def check_gpu_availability(num_gpus=2):
    try:
        free_gpu_ids = []
        while len(free_gpu_ids) < num_gpus:
            # Get the list of available GPUs
            gpus = GPUtil.getGPUs()
            print("All GPU device : ",gpus)

            if not gpus:
                print("No GPU available.")
                return []

            # Check if any GPU is free
            for gpu in gpus:
                if gpu.memoryUsed == 0 and gpu.id not in free_gpu_ids:
                    free_gpu_ids.append(gpu.id)
                    if len(free_gpu_ids) == num_gpus:
                        return free_gpu_ids

            # If not enough GPUs are free, wait for a while before checking again
            print(f"GPU not enough({num_gpus}) finding...")
            time.sleep(1)

    except Exception as e:
        print("Error occurred:", str(e))
        return []

def run_code_on_available_gpu(cli):
    num_gpus_needed = 2
    gpu_ids  = check_gpu_availability(num_gpus_needed)
    if gpu_ids  is not None:
        print("GPU", gpu_ids, "is available. Running code on this GPU.")
        # Call your code that utilizes the GPU here
        try:
            # Execute the command and capture the output
            output = subprocess.check_output(cli, shell=True, universal_newlines=True)
            print("Command output:")
            print(output)
        except subprocess.CalledProcessError as e:
            # Handle errors if the command fails
            print("Error:", e)
    else:
        print("No GPU available. Cannot run code.")

def cli_command(cli = input_cli()):
    run_code_on_available_gpu(cli)


# Call the function to run your code on an available GPU
def main():
    cli_command()
    
    

if __name__ == "__main__":
    main()