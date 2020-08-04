from collections import defaultdict
from pprint import pprint
from random import choices, choice
import math
# const pos_anch_pairs = []
# for every class
# get all pairs

# for every pair
# get pairs with negative

# const triplets = []

# classes_by_angle = {
#     'class1': {
#         'center': [index1, index2],
#         'left': [index1, index2],
#         'right': [index1, index2]
#     }
# }

# 1: center, 2: left, 3: right, : 4 back
angles = ['1', '2', '3', '4']
test_ratio = 0.2


def group_labels_by_angles(all_files_obj):
    '''Groups by and also creates list of all images'''
    labels_by_angle = defaultdict(defaultdict(list).copy)
    images = []
    images_length = 0
    for (index, line) in enumerate(all_files_obj.readlines()):
        image_name = line.rstrip('.jpg\n').replace('static/images/', '')
        images.append(image_name)
        label_id, image_id, angle = image_name.split('_')
        labels_by_angle[label_id][angle].append(index)
        images_length += 1
    num_of_test = int(math.ceil(test_ratio * images_length))
    return(images, labels_by_angle, num_of_test)


def get_negative_indexes(labels_by_angle, label_id, angle):
    '''Returns two negative indexes of the same angle'''
    rest_label_ids = list(labels_by_angle.keys())
    rest_label_ids.remove(label_id)
    label_id_1, label_id_2 = choices(rest_label_ids, k=2)
    negative_index_1 = choice(labels_by_angle[label_id_1][angle])
    negative_index_2 = choice(labels_by_angle[label_id_2][angle])
    return (negative_index_1, negative_index_2)


def get_positive_indexes(label, angle):
    '''Returns two positive indexes of different angle'''
    angle_1 = None
    angle_2 = None
    if (angle == '1'):
        if len(label['2']) > 0:
            angle_1 = '2'
        if len(label['3']) > 0:
            angle_2 = '3'
    if (angle == '2'):
        if len(label['1']) > 0:
            angle_1 = '1'
        if len(label['3']) > 0:
            angle_2 = '3'
    if (angle == '3'):
        if len(label['1']) > 0:
            angle_1 = '1'
        if len(label['2']) > 0:
            angle_2 = '2'
    positive_index_1 = choice(label[angle_1])
    positive_index_2 = choice(label[angle_2])
    return (positive_index_1, positive_index_2)


def generate_triplets():
    '''Generates two triplets for every image.'''
    with open('all_train_files.txt', 'r') as all_files_obj, \
            open('sampled_train_triplets.txt',
                 'a',
                 newline=''
                 ) as train_obj, \
            open('sampled_test_triplets.txt',
                 'a',
                 newline=''
                 ) as test_obj:

        images, labels_by_angle, num_of_test = group_labels_by_angles(
            all_files_obj)
        # print('labels_by_angle: ')
        # pprint(labels_by_angle)

        for (counter, image_name) in enumerate(images):
            anchor_index = counter

            label_id, image_id, angle = image_name.split('_')

            negative_index_1, negative_index_2 = get_negative_indexes(
                labels_by_angle, label_id, angle
            )

            label = labels_by_angle[label_id]
            positive_index_1, positive_index_2 = get_positive_indexes(
                label, angle
            )
            if (counter + 1 <= num_of_test):
                triplet_1 = (
                    f'{anchor_index} '
                    f'{positive_index_1} '
                    f'{negative_index_1}'
                )
                test_obj.write(triplet_1)
                test_obj.write('\n')
                triplet_2 = (
                    f'{anchor_index} '
                    f'{positive_index_2} '
                    f'{negative_index_2}'
                )
                test_obj.write(triplet_2)
                test_obj.write('\n')
            else:
                triplet_1 = (
                    f'{anchor_index} '
                    f'{positive_index_1} '
                    f'{negative_index_1}'
                )
                train_obj.write(triplet_1)
                train_obj.write('\n')
                triplet_2 = (
                    f'{anchor_index} '
                    f'{positive_index_2} '
                    f'{negative_index_2}'
                )
                train_obj.write(triplet_2)
                train_obj.write('\n')
