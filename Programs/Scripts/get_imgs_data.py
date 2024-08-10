from os import listdir
from os.path import isfile, join, getctime

from PIL import Image, ExifTags

from datetime import datetime

from multiprocessing import Pool
from itertools import repeat

def get_time(path):
    with Image.open(path) as image:
        try:
            image_exif = image._getexif()
            
            exif = tuple(v for k, v in image_exif.items() if ExifTags.TAGS[k] == 'DateTimeOriginal')[0]
            #exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
            
            date_obj = datetime.strptime(exif, r'%Y:%m:%d %H:%M:%S').strftime(r'%Y%m%d%H%M%S')
            #date_obj = datetime.strptime(exif['DateTimeOriginal'], r'%Y:%m:%d %H:%M:%S').strftime(r'%Y%m%d%H%M%S')
            return date_obj
        except (KeyError, AttributeError):
            try:
                image_exif = image.getexif()
                date_obj = datetime.strptime(image_exif[306], r'%Y:%m:%d %H:%M:%S').strftime(r'%Y%m%d%H%M%S')
                return date_obj
            except KeyError:
                date_obj = datetime.fromtimestamp(getctime(path)).strftime(r'%Y%m%d%H%M%S')
                return date_obj

def get_img_data(file, directory):
    file_path = join(directory, file)
    file_type = file_path[file_path.find('.'):].upper()
    if (file_type == '.HEIC' or file_type == '.JPEG' or file_type == '.JPG' or file_type == '.PNG') and isfile(file_path):
        return [file_path, file_type, get_time(file_path)]
    else:
        pass

def multi_get_img_data(directory):
    files = listdir(directory)
    
    pool = Pool(5)
    results = pool.starmap(get_img_data, zip(files, repeat(directory)), 5)
    
    return results

def no_threading_get_img_data(directory):
    return tuple(get_img_data(file, directory) for file in listdir(directory))