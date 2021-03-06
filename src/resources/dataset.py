# import sys
from flask_restful import Resource
from models.dataset import DatasetModel
from models.image import ImageModel
import os
import json
import csv
import subprocess
import shutil
from libs.image import crop_bounding_boxes
from libs import annotations


BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "A dataset with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the dataset."
DATASET_NOT_FOUND = "Dataset not found."
DATASET_DELETED = "Dataset deleted."


class Dataset(Resource):
    @classmethod
    def get(cls, name: str):
        dataset = DatasetModel.find_by_name(name)
        if dataset:
            return dataset.json()
        return {"message": DATASET_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if DatasetModel.find_by_name(name):
            return (
                {
                    "message": NAME_ALREADY_EXISTS.format(name),
                    "reason": "name_already_exists"
                },
                400,
            )

        dataset = DatasetModel(name)
        try:
            dataset.save_to_db()
        except Exception:
            return (
                {
                    "message": ERROR_INSERTING,
                    "reason": "error_inserting"
                },
                500
            )

        return dataset.json(), 201

    @ classmethod
    def delete(cls, name: str):
        dataset = DatasetModel.find_by_name(name)
        if dataset:
            dataset.delete_from_db()
            return {"message": DATASET_DELETED}, 200
        return {"message": DATASET_NOT_FOUND}, 404


class DatasetList(Resource):
    @classmethod
    def get(cls):
        return {"datasets": [x.json() for x in DatasetModel.find_all()]}



class DatasetClassify(Resource):
    # @jwt_required
    def get(self):
        # data = image_schema.load(request.files)
        predict_dir = os.path.join(os.getcwd(), '../sku110k/env/bin/activate')
        predict_dir = os.path.abspath(os.path.join(predict_dir, os.pardir))
        os.environ['PYTHONPATH'] = "/opt/rpcserver/sku110k"
        python_bin = os.path.abspath("../sku110k/env/bin/python")
        subprocess.call(
            f'nohup env PYTHONPATH="/opt/rpcserver/sku110k"; . /opt/rpcserver/sku110k/env/bin/activate; python -u /opt/rpcserver/sku110k/object_detector_retinanet/keras_retinanet/bin/predict.py --gpu 3 csv "/opt/rpcserver/sku110k/iou_resnet50_csv_06.h5" --hard_score_rate=0.5 | tee results/predict_sku110k.log', shell=True)
        
        crop_bounding_boxes()

        subprocess.call(
            f'. /opt/rpcserver/encoder/env/bin/activate; python /opt/rpcserver/encoder/test.py --name latest --reranking 2 --test_images_dir results/images --invitro_images_dir /opt/rpcserver/encoder/ref_dir', shell=True)
        # dataset_id = request.form.get("dataset_id")

        return
        # label = LabelModel.find_by_id(label_id)
        # try:
        #     # create image in db
        #     image = ImageModel(angle, dim, metadata, label.id)
        #     # save(self, storage, folder=None, name=None)
        #     try:
        #         image.save_to_db()
        #         # static/images/f'{label.id}_{image.id}_{angle}}
        #         image_path = image_helper.save_image(
        #             data["image"], name=image.name)
        #         # here we only return the basename of the image and hide the
        #         # internal folder structure from our user
        #         basename = image_helper.get_basename(image_path)
        #         with open('annotations.csv', 'a', newline='') as csvfile:
        #             annotationswriter = csv.writer(csvfile)
        #             annotationswriter.writerow(
        #                 [
        #                     basename,
        #                     int(proper_round(bounding_box['top_left']['x'])),
        #                     int(proper_round(bounding_box['top_left']['y'])),
        #                     int(proper_round(
        #                         bounding_box['bottom_right']['x']
        #                     )),
        #                     int(proper_round(
        #                         bounding_box['bottom_right']['y']
        #                     )),
        #                     label.name,
        #                     dimensions['width'],
        #                     dimensions['height']
        #                 ]
        #             )
        #         with open('all_train_files.txt', 'a') as txtObj:
        #             txtObj.write(f'static/images/{image_path}')
        #             txtObj.write('\n')
        #     except UploadNotAllowed:  # forbidden file type
        #         extension = image_helper.get_extension(data["image"])
        # return {"message": IMAGE_ILLEGAL_EXTENSION.format(extension)}, 400
        # except Exception:
        #     print("Exception", Exception)
        #     print("Unexpected error:", sys.exc_info()[0])
        #     raise
        #     return {"message": ERROR_INSERTING}, 500

        # return {"message": IMAGE_UPLOADED.format(image.name)}, 201


class DatasetTrain(Resource):
    def get(self, id: int):
        dataset = DatasetModel.find_by_id(id)
        labels = dataset.labels
        labels = [label for label in labels.all()]
        with open('annotations.csv', 'w', newline='') as csvfile, \
            open('all_train_files_new.txt', 'w') as txtObj, \
            open('../sku110k/object_detector_retinanet/keras_retinanet/bin/class_mappings.csv', 'a', newline='') as classMap:
                for label in labels:
                    classMapWriter = csv.writer(classMap)
                    classMapWriter.writerow([label.id,label.id])
                    images = ImageModel.find_by_label_id(label.id)
                    for image in images:
                        # shutil.copy(f'static/images/{image.name}', '../sku110k/images')
                        meta_data = json.loads(image.meta_data)
                        dimensions = json.loads(image.dimensions)
                        bounding_box = meta_data['bounding_box']

                        annotationswriter = csv.writer(csvfile)
                        annotationswriter.writerow(
                            [
                                image.name,
                                round(bounding_box['top_left']['x']),
                                round(bounding_box['top_left']['y']),
                                round(
                                    bounding_box['bottom_right']['x']
                                ),
                                round(
                                    bounding_box['bottom_right']['y']
                                ),
                                label.id,
                                dimensions['width'],
                                dimensions['height']
                            ]
                        )
                        txtObj.write(f'static/images/{image.name}')
                        txtObj.write('\n')
        annotations.train_val_test_split()
        os.environ['PYTHONPATH'] = "../sku110k"
        subprocess.call(f'nohup env PYTHONPATH="../sku110k"; . ../sku110k/env/bin/activate; python -u ../sku110k/object_detector_retinanet/keras_retinanet/bin/train.py --weights ../sku110k/iou_resnet50_csv_06.h5 csv', shell=True)

        
        # crop_bounding_boxes()
        return
