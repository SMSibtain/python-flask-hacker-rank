import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.store import Store, StoreList
from resources.user import Auth, UserRegister
from resources.item import Items, ItemList
from datetime import timedelta

app = Flask(__name__)

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
api = Api(app)

jwt = JWTManager(app)  # , authenticate, identity)  # /auth

api.add_resource(Auth, '/auth')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
