import subprocess, os, urllib.request, json

github_account = "acipensersturio"
github_repo = "test_repo_4"
path_temp_folder = "temp/"
path_vol_folder = "temp/vol/"
path_json_folder = "temp/json/"
path_outer = "in/outer.zip"
path_ascii = "temp/ascii.txt"
path_out = "out/outer.zip"
files_count = 101
urls = []

def get_page(url, filepath):
    contents = urllib.request.urlopen(url).read()
    with open(filepath, 'wb') as file:
        file.write(contents)
def save_page(url):
    contents = urllib.request.urlopen(url).read()
    print(url, "saved")

# Method used for splitting files
def split_file(input_file, output_folder, output_file_ext = ".html", chunk_size = 2**20):
    file_number = 0
    with open(input_file, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk != b'':
            file_path = output_folder + str(file_number) + output_file_ext
            with open(file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunk_size)
    return file_number

def join_files(file_number, output_file, input_folder, input_file_ext = ".html"):
    with open(output_file, 'wb') as out:
        for file in range(file_number):
            file_path = input_folder + str(file) + input_file_ext
            with open(file_path, 'rb') as f:
                chunk = f.read()
                print(out.write(chunk))


def uploading_to_wayback():
    # Create output folder, if it doesn't already exist
    if not os.path.exists(path_temp_folder):
        os.mkdir(path_temp_folder)
    if not os.path.exists(path_vol_folder):
        os.mkdir(path_vol_folder)
    # Get ascii from file
    subprocess.run("encode.exe " + path_outer + " " + path_ascii)
    # Split ascii into multiple html pages
    split_file(path_ascii, path_vol_folder, chunk_size = 2**20)
    # Remove ascii
    os.remove(path_ascii)
    # Upload html pages to github
    subprocess.call("git.bat " + github_account + " " + github_repo)

def downloading_from_wayback():
    # Create output folder, if it doesn't already exist
    if not os.path.exists(path_temp_folder):
        os.mkdir(path_temp_folder)
    if not os.path.exists(path_vol_folder):
        os.mkdir(path_vol_folder)
    if not os.path.exists(path_json_folder):
        os.mkdir(path_json_folder)
    # Get snapshot links using Wayback's API
    for i in range(files_count):
        get_page("https://archive.org/wayback/available?url=https://" + github_account + ".github.io/" + github_repo + "/" + str(i) + ".html", path_json_folder + str(i) + ".html")
        with open(path_json_folder + str(i) + ".html") as file:
            jsondata = json.loads(file.read())
            urls.append(jsondata["archived_snapshots"]["closest"]["url"].replace("/https://", "if_/https://"))
    for url in urls:
        print (url)
    # Download pages
    for i in range(len(urls)):
        get_page(urls[i], path_vol_folder + str(i) + ".html")
        print(urls[i], "downloaded")
    # Count html pages
    html_files = os.listdir(path = path_vol_folder)
    file_number = len(html_files)
    # Join html pages into one ascii
    join_files(file_number, path_ascii, path_vol_folder)
    # Remove html pages
    for page in html_files:
        os.remove(path_vol_folder + page)
    # Get file from ascii
    subprocess.run("decode.exe " + path_ascii + " " + path_out)
    # Remove ascii
    os.remove(path_ascii)
    
