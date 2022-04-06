import os
from flask import Flask
from flask_restful import Api, marshal
from flask_jwt_extended import JWTManager
from resources.store import Store, StoreList
from resources.user import Auth, UserRegister
from resources.item import Items, ItemList
from resources.trades import Trade, Trades
from datetime import timedelta
from db import db
from ma import ma

app = Flask(__name__)


def init_db():
    db.drop_all()
    db.create_all()


uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


if uri:
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "smsrn123"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
# app.secret_key = 'smsrn123'
db.init_app(app)
ma.init_app(app)
api = Api(app)

jwt = JWTManager(app)  # , authenticate, identity)  # /auth

api.add_resource(Auth, '/auth')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Trades, '/trades')
api.add_resource(Trade, '/trades/<string:id>')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
