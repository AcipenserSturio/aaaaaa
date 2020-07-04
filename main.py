import subprocess, os, urllib.request

input_file = 'archivedtwice.zip'
output_folder = 'temp/fromWayback'
temp_file_name = 'temp/temp.txt'
downloaded_ascii = 'temp_transformed'
final_output = 'regained.zip'
urls = ["https://web.archive.org/web/20200621143517if_/https://acipensersturio.github.io/test_repo/1.html",
        "https://web.archive.org/web/20200621143622if_/https://acipensersturio.github.io/test_repo/2.html",
        "https://web.archive.org/web/20200621134704if_/https://acipensersturio.github.io/test_repo/3.html",
        "https://web.archive.org/web/20200621141255if_/https://acipensersturio.github.io/test_repo/4.html"]
def get_page(url, filename):
    contents = urllib.request.urlopen(url).read()
    with open(filename, 'wb') as file:
        file.write(contents)

# Method used for splitting files
def split_file(input_file, output_folder, output_file_name='', output_file_ext = ".html", chunk_size = 2**20):
    file_number = 0
    with open(input_file, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk != b'':
            file_path = output_folder + "/" + output_file_name + str(file_number) + output_file_ext
            with open(file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunk_size)
    return file_number

def join_files(file_number, output_file, input_folder, input_file_name='', input_file_ext = ".txt"):
    with open(output_file, 'wb') as out:
        for file in range(file_number):
            file_path = input_folder + "/" + input_file_name + str(file) + input_file_ext
            with open(file_path, 'rb') as f:
                chunk = f.read()
                print(out.write(chunk))

def file_to_ascii_to_github():
    # Create output folder, if it doesn't already exist
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    # Get ascii from file
    subprocess.run("encode.exe " + input_file + " " + temp_file_name)
    # Split ascii into multiple html pages
    split_file(temp_file_name, output_folder, chunk_size = 2**23)
    # Remove ascii
    os.remove(temp_file_name)
    # Upload html pages to github
    subprocess.run("git.bat")

def ascii_to_file():
    # Download pages
    for i in range(len(urls)):
        get_page(urls[i], output_folder + "/" + str(i) + ".txt")
        print(urls[i] + "downloaded")
    # Count html pages
    html_files = os.listdir(path = output_folder)
    file_number = len(html_files)
    # Join html pages into one ascii
    join_files(file_number, downloaded_ascii, output_folder)
    # Remove html pages
    for page in html_files:
        os.remove(output_folder + "/" + page)
    # Get file from ascii
    subprocess.run("decode.exe " + downloaded_ascii + " " + final_output)
    # Remove ascii
    os.remove(downloaded_ascii)
    
