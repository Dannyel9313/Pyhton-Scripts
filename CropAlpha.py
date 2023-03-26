#!/usr/bin/python
import numpy as np
import os
import glob
import sys
import fnmatch
import argparse
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument("element", help="name of the element for offset coords",
                    type=str)
parser.add_argument("format", help="format of input pictures",
                    type=str)
args = parser.parse_args()

def write_new_coords(anim_name, x, y, width, height):
    output_file_coords.writelines('<Element key="{0}" dest_x="{1}" dest_y="{2}" width="{3}" height="{4}" />\n'.format(anim_name, x, y, width, height))

def element_count(img_count,count):
    if img_count < 100: 
        if count < 10:
            return "0{}".format(count)
        else:
            return "{}".format(count)
    else:
        if count < 10:
            return "00{}".format(count)
        elif count < 100:
            return "0{}".format(count)
        else:
            return "{}".format(count)

def make_cropped_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def crop(image_name,output_name,img_count,current_img,image_format):
    image = Image.open(image_name)
    origin_width,origin_height = image.size
    np_array = np.array(image)
    blank_px = [0, 0, 0, 0]
    mask = np_array != blank_px
    coords = np.argwhere(mask)
    if coords.size == 0:
        print('File : {} is all transparent !!!'.format(image_name))
    else:
        x0, y0, z0 = coords.min(axis=0)
        x1, y1, z1 = coords.max(axis=0) + 1
        if (x1 - x0) % 2 != 0 and x0 != 0:
            x0 -=1
        elif (x1 - x0) % 2 != 0 and x1 != origin_width:
            x1 +=1
        if (y1 - y0) % 2 != 0 and y0 != 0:
            y0 -=1
        elif (y1 - y0) % 2 != 0 and y1 != origin_height:
            y1 +=1
        cropped_box = np_array[x0:x1, y0:y1, z0:z1]
        image = Image.fromarray(cropped_box, 'RGBA')
        new_width, new_height = image.size
        element_key = list_args[1] + "_" + element_count(img_count, current_img) + "_ELEMENT"
        write_new_coords(element_key,y0, x0, new_width, new_height)
        image.save(output_name+".png",format=image_format)

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


list_args = sys.argv
image_format = list_args[2]
directory_path = os.getcwd()
files = os.path.join(directory_path, "*"+image_format)
file_count = len(fnmatch.filter(os.listdir(directory_path), '*'+image_format))

new_directory = directory_path + "/cropped_images"
make_cropped_directory(new_directory)

output_file_coords = open("coords.txt", "w")
count = 0
for filename in sorted(glob.glob(files)):
    base=os.path.basename(filename)
    output_name = filename[:filename.find(base)] + "cropped_images" + "/" + base.split('.')[0]
    crop(filename,output_name,file_count, count, image_format)
    count+=1
    progress(count,file_count)
    
output_file_coords.close()
