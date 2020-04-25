from typing import Dict, List, Union
from db import db

PhotoJSON = Dict[str, Union[int, str, float]]


class PhotoModel(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    label_id = db.Column(db.Integer, db.ForeignKey("labels.id"))
    label = db.relationship("LabelModel")

    def __init__(self, name: str, price: float, label_id: int):
        self.name = name
        self.price = price
        self.label_id = label_id

    def json(self) -> PhotoJSON:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "label_id": self.label_id,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "PhotoModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["PhotoModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
