from ast import parse
from datetime import datetime
from multiprocessing import connection
from random import choices
from sqlite3 import Timestamp
from time import time
from tokenize import String
from flask import jsonify, request
from flask_restful import Resource, reqparse
from models.trade import TradeModel
from db import db
import json
from datetime import datetime
from ma import ma


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return (str(z))
        else:
            return super().default(z)


class Trades(Resource):
    parser = reqparse.RequestParser()
    # FILTER REQUIRED PAYLOAD USING PARSING - START
    parser.add_argument('type',
                        type=str,
                        required=True,
                        choices=["buy", "sell"],
                        location='json')
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('symbol',
                        type=str,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('shares',
                        type=int,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('timestamp',
                        required=True,
                        help="This field can not be left black!")

    # FILTER REQUIRED PAYLOAD USING PARSING - START

    def post(self):
        data = Trades.parser.parse_args()
        # timestamp, ms = divmod(data['timestamp'], 1000)

        data['timestamp'] = datetime.fromtimestamp(
            int(data['timestamp']) / 1000)

        trade = TradeModel(**data)
        trade.save_to_db()
        return {"data":  trade.json()}, 201

    def get(self):
        return {'data': [x.json() for x in TradeModel.query.all()]}


class Trade(Resource):
    parser = reqparse.RequestParser()
    # FILTER REQUIRED PAYLOAD USING PARSING - START
    parser.add_argument('type',
                        type=str,
                        required=True,

                        choices=["buy", "sell"])
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('symbol',
                        type=str,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('shares',
                        type=int,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help="This field can not be left black!")
    # parser.add_argument('timestamp',
    #                     type=datetime,
    #                     required=True,
    #                     help="This field can not be left black!")

    # FILTER REQUIRED PAYLOAD USING PARSING - START

    def get(self, id):
        item = TradeModel.find_by_id(id)

        if item:
            return {'data': item.json()}, 200
        return {'message': 'Item not found'}

    def delete(self, id):
        item = TradeModel.find_by_id(id)

        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}

    def put(self, id):
        data = request.get_json()
        trade = TradeModel(**data)
        item = TradeModel.find_by_id(id)

        if item is None:
            item = TradeModel(**data)  # data['price'], data['store_id'])
        else:
            item = TradeModel(**data)
            item.id = id

        item.save_to_db()
        return item.json()

    def patch(self, id):
        data = request.get_json()
        trade = TradeModel(**data)
        item = TradeModel.find_by_id(id)

        if item is None:
            item = TradeModel(**data)  # data['price'], data['store_id'])
        else:
            item = TradeModel(**data)
            item.id = id

        item.save_to_db()
        return item.json()
