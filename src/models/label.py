from typing import Dict, List, Union
from db import db
from models.image import ImageJSON

LabelJSON = Dict[str, Union[int, str, List[ImageJSON]]]


class LabelModel(db.Model):
    __tablename__ = "labels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    gtin = db.Column(db.Integer, unique=True)

    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"))
    dataset = db.relationship("DatasetModel")
    images = db.relationship("ImageModel", lazy="dynamic")

    def __init__(self, name: str, gtin: int, dataset_id: int):
        self.name = name
        self.gtin = gtin
        self.dataset_id = dataset_id

    def json(self) -> LabelJSON:
        return {
            "id": self.id,
            "name": self.name,
            "gtin": self.gtin,
            "dataset_id": self.dataset_id,
            "image_ids": [image.json()["id"] for image in self.images.all()],

        }

    @classmethod
    def find_by_name(cls, name: str) -> "LabelModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_gtin(cls, gtin: int) -> "LabelModel":
        return cls.query.filter_by(gtin=gtin).first()

    @classmethod
    def find_by_id(cls, id: int) -> "LabelModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List["LabelModel"]:
        return cls.query.all()

    @classmethod
    def find_by_dataset_id(cls, dataset_id: int) -> List["LabelModel"]:
        return cls.query.filter_by(dataset_id=dataset_id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
