import os
import csv
import shutil
from PIL import Image
import argparse
import sys


def extract_products_from_scenes():

    with open('annotations.csv', "r") as f:
        f_counter = csv.reader(f, delimiter=',')
        row_count = sum(1 for row in f_counter)

    with open('annotations.csv', "r") as f_all:
        f_all_reader = csv.reader(f_all, delimiter=',')
        i = 0
        total_counter = 0
        print("Extracting and reformatting products from scene, according to the bounding-box-CSV you supplied/was generated in the Product Detection step...")
        for row in f_all_reader:
            name = row[0]
            filename = os.path.join('static/images/Lotus', name)
            im = Image.open(filename)
            x1 = int(float(row[1]))
            y1 = int(float(row[2]))
            x2 = int(float(row[3]))
            y2 = int(float(row[4]))
            im = im.crop((x1, y1, x2, y2))
            x, y = im.size
            ratio = 512.0/max(x, y)
            new_x = x*ratio
            new_y = y*ratio
            new_im = Image.new('RGB', (512, 512), (0, 0, 0, 0))
            resized_im = im.resize((int(new_x), int(new_y)), Image.BICUBIC)
            new_im.paste(
                resized_im, (int((512 - new_x) / 2), int((512 - new_y) / 2)))
            new_im.save('img' + "/" + name + ".png", "PNG")
            total_counter += 1
            progressBar(total_counter, row_count)
        print("\nDone extracting.\n")


def progressBar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r[{0}] {1}%".format(
        arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()
