from typing import Dict, List, Union
from db import db

ImageJSON = Dict[str, Union[int, str, float]]


class ImageModel(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    angle = db.Column(db.String(80))
    dimensions = db.Column(db.String(800))
    meta_data = db.Column(db.String(2000))

    label_id = db.Column(db.Integer, db.ForeignKey("labels.id"))
    label = db.relationship("LabelModel")

    def __init__(
        self,
        angle: str,
        dimensions: str,
        meta_data: str,
        label_id: int
    ):
        self.name = f'{self.id}_{label_id}.jpg'
        self.angle = angle
        self.dimensions = dimensions
        self.meta_data = meta_data
        self.label_id = label_id

    def json(self) -> ImageJSON:
        return {
            "id": self.id,
            "angle": self.angle,
            "name": self.name,
            "dimensions": self.dimensions,
            "meta_data": self.meta_data,
            "label_id": self.label_id,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "ImageModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id: str) -> "ImageModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_label_id(cls, label_id: int) -> List["ImageModel"]:
        return cls.query.filter_by(label_id=label_id)

    @classmethod
    def find_all(cls) -> List["ImageModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.flush()
        self.name = f'{self.label_id}_{self.id}_{self.angle}.jpg'
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
