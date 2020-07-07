import os
import csv
import math
import random


current_directory = os.getcwd()
folder = os.path.join(current_directory, r'annotations')
if not os.path.exists(folder):
    os.makedirs(folder)


def train_val_test_split():
    with open('annotations.csv') as annotations_file, \
            open(f'{folder}/annotations_train.csv',
                 'a',
                 newline=''
                 ) as train_file, \
            open(f'{folder}/annotations_val.csv',
                 'a',
                 newline=''
                 ) as val_file, \
            open(f'{folder}/annotations_test.csv',
                 'a',
                 newline=''
                 ) as test_file:

        annotations_reader = csv.reader(annotations_file, delimiter=',')
        train_writer = csv.writer(train_file)
        val_writer = csv.writer(val_file)
        test_writer = csv.writer(test_file)

        train_ratio = 0.8
        test_ratio = 1 - train_ratio

        annotations = list(annotations_reader)
        annotations_length = len(annotations)
        print("annotations_length", annotations_length)

        random.shuffle(annotations)

        num_of_test = int(math.ceil(test_ratio * annotations_length))
        num_of_val = num_of_test
        num_of_train = int(math.ceil(train_ratio * annotations_length))
        print("num_of_val", num_of_val)
        print("num_of_train", num_of_train)

        annotations_file.seek(0)
        test = []
        val = []
        train = []

        for counter, row in enumerate(annotations):
            print("counter", counter)
            if counter + 1 <= num_of_test:
                # print('Test: ')
                # print(', '.join(row))
                test_writer.writerow(row)
                test.append(row)
            elif counter + 1 <= num_of_val * 2:
                val_writer.writerow(row)
                val.append(row)
            else:
                train_writer.writerow(row)
                train.append(row)

        print("Number of lines in the annotations.csv: ", annotations_length)
        print("Number of lines in the annotations_train.csv: ", num_of_train)
        print("Number of lines in the annotations_val.csv: ", num_of_val)

        print("\n")
        print("Train: ")
        [print(', '.join(row)) for row in train]
        print("\n")
        print("Validation: ")
        [print(', '.join(row)) for row in val]
        print("\n")
        print("Test: ")
        [print(', '.join(row)) for row in test]
        print("\n")
