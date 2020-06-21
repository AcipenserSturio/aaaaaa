import subprocess, os

# Method used for splitting files
def split_file(input_file, output_folder, output_file_name='', output_file_ext = ".html", chunk_size = 2**20):
    file_number = 1
    with open(input_file, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk != b'':
            file_path = output_folder + "/" + output_file_name + str(file_number) + output_file_ext
            with open(file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunk_size)
    return file_number

# 
input_file = 'archivedtwice.zip'
output_folder = 'temp'
temp_file_name = "temp/temp.txt"

if not os.path.exists(output_folder):
    os.mkdir(output_folder)
subprocess.run("encode.exe " + input_file + " " + temp_file_name)
file_number = split_file(temp_file_name, output_folder, chunk_size = 2**25)
os.remove(temp_file_name)
# subprocess.run("git.bat")
