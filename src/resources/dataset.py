from flask_restful import Resource
from models.dataset import DatasetModel

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
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400,

        dataset = DatasetModel(name)
        try:
            dataset.save_to_db()
        except Exception:
            return {"message": ERROR_INSERTING}, 500

        return dataset.json(), 201

    @classmethod
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
