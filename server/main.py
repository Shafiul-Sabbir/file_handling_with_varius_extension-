import shutil
import zipfile
import os
import glob
import subprocess

source_path = '../source'
destination_path = '../destination'
param_list = [1, 2, 3]

# Create destination directory if it doesn't exist
os.makedirs(destination_path, exist_ok=True)

# Find and copy .txt files, and run .py files
for source_file in glob.glob(os.path.join(source_path, '*.txt')):
    filename = os.path.basename(source_file)
    prefix, _ = os.path.splitext(filename)

    # Copy .txt files and modify content
    for i in param_list:
        new_filename = f'{prefix}_{i}.txt'
        destination_file = os.path.join(destination_path, new_filename)
        num_of_lines = i * 10  # Calculate the number of lines

        # Generate and write modified content to destination file
        with open(source_file, 'r') as source_f, open(destination_file, 'a') as dest_f:
            for j in range(num_of_lines):
                dest_f.write(source_f.read() + f' - Line {j + 1}\n')

    # Run .py files and capture output and errors
    if filename.endswith('.py'):
        try:
            result = subprocess.run(['python', source_file], text=True, capture_output=True, check=True)
            print(f"Output of {filename}:\n{result.stdout}")
            if result.stderr:
                print(f"Errors of {filename}:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error running {filename}:\n{e.stderr}")

# Create a zip archive of the destination directory
with zipfile.ZipFile(os.path.join(destination_path, 'destination.zip'), 'w') as zipf:
    for root, _, files in os.walk(destination_path):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), destination_path))

print("Performed successfully !!!")

# Unzip the archive after sending (assuming it's received and saved in the destination folder)
zip_path = os.path.join(destination_path, 'destination.zip')
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(destination_path)
    