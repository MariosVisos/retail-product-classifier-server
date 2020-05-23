from typing import Dict, List, Union
from db import db

ImageJSON = Dict[str, Union[int, str, float]]


class ImageModel(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    label_id = db.Column(db.Integer, db.ForeignKey("labels.id"))
    label = db.relationship("LabelModel")

    def __init__(self, name: str, label_id: int):
        self.name = name
        self.label_id = label_id

    def json(self) -> ImageJSON:
        return {
            "id": self.id,
            "name": self.name,
            "label_id": self.label_id,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "ImageModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_label_id(cls, label_id: int) -> List["ImageModel"]:
        return cls.query.filter_by(label_id=label_id)

    @classmethod
    def find_all(cls) -> List["ImageModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
