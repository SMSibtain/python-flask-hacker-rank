from datetime import datetime
from email.policy import default
import string
from db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class TradeModel(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    user_id = db.Column(db.Integer)
    symbol = db.Column(db.String)
    shares = db.Column(db.Integer)
    price = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    # def json(self):
    # return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def json(self, *excludeFields):
        return TradeSchema(exclude=list(excludeFields)).dump(self)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self):
        return self.query.all()


class TradeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TradeModel
        # load_instance = True
