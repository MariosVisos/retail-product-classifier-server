from typing import Dict, List, Union
from db import db
from models.image import ImageJSON

LabelJSON = Dict[str, Union[int, str, List[ImageJSON]]]


class LabelModel(db.Model):
    __tablename__ = "labels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"))
    dataset = db.relationship("DatasetModel")
    images = db.relationship("ImageModel", lazy="dynamic")

    def __init__(self, name: str, price: float, dataset_id: int):
        self.name = name
        self.price = price
        self.dataset_id = dataset_id

    def json(self) -> LabelJSON:
        return {
            "id": self.id,
            "name": self.name,
            "dataset_id": self.dataset_id,
            "images": [image.json() for image in self.images.all()],

        }

    @classmethod
    def find_by_name(cls, name: str) -> "LabelModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["LabelModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
