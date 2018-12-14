import os
import glob
from shutil import copyfile, make_archive, rmtree
import zipfile

fixing_directory = "epubs/"
fixed_directory = "fixed_epubs/" #recommended outside of the orig dir

def init():
    global fixing_directory,completed_directory
    os.makedirs(fixing_directory, exist_ok=True)
    os.makedirs(fixed_directory, exist_ok=True)

def clean_epubs():
    global remainding
    epub_locations = find_epubs()
    if epub_locations != []:
        folder_locations = unpack_epubs(epub_locations)
        try:
            for folder_location in folder_locations:
                try:
                    fix_epub_issues(folder_location)
                    compress_and_convert_to_epub(folder_location)
                    remainding -= 1
                except Exception as e:
                    print("Fixing Error!",e)
                    remainding -= 1
        except Exception as e:
            print("Fixing Error!",e)
    print("Complete.")

def unpack_epubs(epub_locations):
    global total,remainding
    try:
        os.stat(fixing_directory)
        try:
            total = len(epub_locations)
        except:
            total = 0
        if total == 1:
            print("Attempting to fix {} EPUB...".format(total))
        else:
            print("Attempting to fix {} EPUBs...".format(total))
        remainding = total
        if epub_locations != []:
            zip_locations = []
            for epub_location in epub_locations:
                print("Decrypting {}".format(epub_location.split("\\")[-1]))
                zip_location = epub_location.replace(".epub",".zip")
                copyfile(epub_location, zip_location)
                zip_locations.append(zip_location)
            folder_locations = []
            for zip_location in zip_locations:
                print("Uncompressing {}".format(zip_location.split("\\")[-1]))
                with zipfile.ZipFile(zip_location, 'r') as zip_ref:
                    zip_directory_extracted = zip_location.replace(".zip","\\")
                    try:
                        os.stat(zip_directory_extracted)
                    except:
                        os.mkdir(zip_directory_extracted)
                    zip_ref.extractall(zip_directory_extracted)
                    folder_locations.append(zip_directory_extracted)
                os.remove(zip_location)
            return folder_locations
    except FileNotFoundError:
        os.mkdir(fixing_directory)
        print("No Directory!")
    except Exception as e:
        print("Error!",e)

def fix_epub_issues(folder_location):
    global total,remainding
    print("Progress:",str(round(((total-remainding)/total)*100,2))+"%")
    if remainding == 1:
        print("{} EPUB left".format(remainding))
    else:
        print("{} EPUBs left".format(remainding))
    print("Fixing...")
    for xhtml in glob.iglob(folder_location + '**/**.xhtml', recursive=True):
        with open(xhtml, "r", encoding="UTF-8") as file: #potentially slow
            data = file.read().replace('&amp;quot;', '"')
            with open(xhtml, "w", encoding="UTF-8") as file2:
                file2.write(data)

def compress_and_convert_to_epub(folder_location):
    global fixed_directory
    new_zip_name = folder_location.split("\\")[-2]
    output_location = fixed_directory+new_zip_name
    make_archive(output_location, 'zip', folder_location)
    rmtree(folder_location)
    try:
        os.rename(output_location+".zip",output_location+"_fixed.epub")
    except:
        print("yeet")
    print("Fixed:",output_location+"_fixed.epub")

def find_epubs():
    global fixing_directory
    epub_locations = []
    for filename in glob.iglob(fixing_directory + '**/**.epub', recursive=True):
        print("Found:",filename)
        epub_locations.append(filename)
    if epub_locations != []:
        #do something with that knowledge
        pass
    else:
        print("Nothing to unpack! Try placing EPUB files in the \"{}\" directory.".format(fixing_directory))
    return epub_locations

init()
clean_epubs()
