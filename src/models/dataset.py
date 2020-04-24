from typing import Dict, List, Union
from db import db
from models.label import LabelJSON

DatasetJSON = Dict[str, Union[int, str, List[LabelJSON]]]


class DatasetModel(db.Model):
    __tablename__ = "datasets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    labels = db.relationship("LabelModel", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self) -> DatasetJSON:
        return {
            "id": self.id,
            "name": self.name,
            "labels": [label.json() for label in self.labels.all()],
        }

    @classmethod
    def find_by_name(cls, name: str) -> "DatasetModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["DatasetModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
