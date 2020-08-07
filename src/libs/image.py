import os
import csv
from PIL import Image
import sys

def crop_bounding_boxes():
    # csv = annotations.csv
    if not os.path.isfile('annotations.csv'):
        with open("annotations.csv", "w") as empty_csv:
            pass 
    if not os.path.isdir('img'):
        os.mkdir("img")
    
    with open("annotations.csv", "r") as f:
        f_counter = csv.reader(f, delimiter=',')
        row_count = sum(1 for row in f_counter)

    with open("annotations.csv", "r") as f_all:
        f_all_reader = csv.reader(f_all, delimiter=',')
        i = 0
        total_counter = 0
        # next(f_all_reader, None)
        print("Extracting and reformatting products from scene, according to the bounding-box-CSV you supplied/was generated in the Product Detection step...")
        for row in f_all_reader:
            print("row", row)
            name = row[0]
            filename = os.path.join('static/images', name)
            # filename = os.path.join(os.getcwd(), name)
            im = Image.open(filename)
            x1 = int(float(row[1]))
            print("x1", x1)
            y1 = int(float(row[2]))
            print("y1", y1)
            x2 = int(float(row[3]))
            print("x2", x2)
            y2 = int(float(row[4]))
            print("y2", y2)
            im = im.crop((x1, y1, x2, y2))
            x, y = im.size
            ratio = 512.0/max(x, y)
            new_x = float("{:.12f}".format(x*ratio))
            print("x", x)
            print("y", y)
            print("ratio", ratio)
            new_y = y*ratio
            print("new_x", new_x)
            print("new_y", new_y)
            new_im = Image.new('RGB', (512, 512), (0, 0, 0, 0))
            print("new_im", new_im)
            resized_im = im.resize((int(new_x), int(new_y)), Image.BICUBIC)
            new_im.paste(
                resized_im, (int((512 - new_x) / 2), int((512 - new_y) / 2)))
            # filepath, extension = name.split(".")
            # output_path = f"results/{filepath}({total_counter}).{extension}"
            # new_im.save(output_path)
            new_im.save('img' + "/" + name)
            total_counter += 1
            progressBar(total_counter, row_count)
        print("\nDone extracting.\n")


def progressBar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r[{0}] {1}%\n".format(
        arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()
