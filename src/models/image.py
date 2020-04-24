from db import db


class ImageModel(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    label_id = db.Column(db.Integer, db.ForeignKey("labels.id"))
    label = db.relationship("LabelModel")

    def __init__(self, name, price, label_id):
        self.name = name
        self.price = price
        self.label_id = label_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "label_id": self.label_id,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
