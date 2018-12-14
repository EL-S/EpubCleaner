import os
import glob
from shutil import copyfile
import zipfile

directory = "epubs/"

def clean_epubs():
    folder_locations = unpack_epubs()
    try:
        for folder_location in folder_locations:
            fix_epub_issues(folder_location)
    except:
        print("Fixing Error!")

def unpack_epubs():
    try:
        os.stat(directory)
        epub_locations = find_epubs()
        print(epub_locations)
        if epub_locations != []:
            zip_locations = []
            for epub_location in epub_locations:
                zip_location = epub_location.replace(".epub",".zip")
                copyfile(epub_location, zip_location)
                zip_locations.append(zip_location)
            folder_locations = []
            for zip_location in zip_locations:
                with zipfile.ZipFile(zip_location, 'r') as zip_ref:
                    zip_directory_extracted = zip_location.replace(".zip","")
                    try:
                        os.stat(zip_directory_extracted)
                    except:
                        os.mkdir(zip_directory_extracted)
                    zip_ref.extractall(zip_directory_extracted)
                    folder_locations.append(zip_directory_extracted)
                    fix_epub_issues
                    print(zip_directory_extracted)
            return folder_locations
    except FileNotFoundError:
        os.mkdir(directory)
        print("No directory!")
    except Exception as e:
        print("Error!",e)

def fix_epub_issues(folder_location):
    for xhtml in glob.iglob(folder_location + '**/**.xhtml', recursive=True):
        print(xhtml)
        with open(xhtml, "r+") as file:
            data = file.read().replace("&amp;quot;", "\"")
            with open(xhtml, "w") as file2:
                file.write(data)

def find_epubs():
    global directory
    epub_locations = []
    for filename in glob.iglob(directory + '**/**.epub', recursive=True):
        print(filename)
        epub_locations.append(filename)
    if epub_locations != []:
        #do something with that knowledge
        pass
    else:
        print("Nothing to unpack!")
    return epub_locations

clean_epubs()
