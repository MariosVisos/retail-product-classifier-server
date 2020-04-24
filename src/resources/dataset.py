from flask_restful import Resource
from models.dataset import DatasetModel


class Dataset(Resource):
    @classmethod
    def get(cls, name: str):
        dataset = DatasetModel.find_by_name(name)
        if dataset:
            return dataset.json()
        return {"message": "Dataset not found."}, 404

    @classmethod
    def post(cls, name: str):
        if DatasetModel.find_by_name(name):
            return (
                {"message": "A dataset with name '{}' already exists.".format(
                    name)},
                400,
            )

        dataset = DatasetModel(name)
        try:
            dataset.save_to_db()
        except:
            return {"message": "An error occurred while creating the dataset."}, 500

        return dataset.json(), 201

    @classmethod
    def delete(cls, name: str):
        dataset = DatasetModel.find_by_name(name)
        if dataset:
            dataset.delete_from_db()

        return {"message": "Dataset deleted."}


class DatasetList(Resource):
    @classmethod
    def get(cls):
        return {"datasets": [x.json() for x in DatasetModel.find_all()]}
