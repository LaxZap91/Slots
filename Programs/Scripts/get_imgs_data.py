from os import listdir
from os.path import isfile, join, getctime

from PIL import Image, ExifTags

from datetime import datetime

from threading import Thread


def get_time(path):
    try:
        with Image.open(path) as image:
            try:
                image_exif = image.getexif()
                exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if
                        k in ExifTags.TAGS and type(v) is not bytes}
                date_obj = datetime.strptime(exif['DateTimeOriginal'], r'%Y:%m:%d %H:%M:%S').strftime(r'%Y%m%d%H%M%S')
                return date_obj
            except (KeyError, AttributeError):
                try:
                    image_exif = image.getexif()
                    date_obj = datetime.strptime(image_exif[306], r'%Y:%m:%d %H:%M:%S').strftime(r'%Y%m%d%H%M%S')
                    return date_obj
                except KeyError:
                    date_obj = datetime.fromtimestamp(getctime(path)).strftime(r'%Y%m%d%H%M%S')
                    return date_obj
                except Exception:
                    print(f"Cannot get date for {path}")
    except Exception as e:
        print(f"Cannot open {path} because {e}")


def get_img_data(file, directory):
    file_path = join(directory, file)
    file_type = file_path[file_path.find('.'):].upper()
    if (file_type == '.HEIC' or file_type == '.JPEG' or file_type == '.JPG' or file_type == '.PNG') and isfile(
            file_path):
        if (file_time := get_time(file_path)) is not None:
            return [file_path, file_type, file_time]


def multi_get_img_data(directory):
    files = listdir(directory)

    threads = []
    results = []

    def get_data_thread(file):
        results.append(get_img_data(file, directory))

    for file in files:
        thread = Thread(target=get_data_thread, args=(file,), daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


def no_threading_get_img_data(directory):
    return tuple(get_img_data(file, directory) for file in listdir(directory))
