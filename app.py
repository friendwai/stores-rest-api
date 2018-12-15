from flask import Flask # request  # not needing moving to item.py
from flask_restful import Api # Resource , reqparse # not needing moving to item.py
from flask_jwt import JWT # jwt_required  # not needing moving to item.py

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

# import sqlite3
#
# connection = sqlite3.connect('data.db')
# cursor = connection.cursor()
#
# create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
# cursor.execute(create_table)
#
# create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
# cursor.execute(create_table)
#
# # cursor.execute("INSERT INTO items VALUES('test', 10.99)") # no longer need test items
#
# connection.commit()
#
# connection.close()
#SQLalchemy can create table hence deleted create_table.py(code above from the file)
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity) # /auth

# items = [] # not using local memory database
# moving to item.py
# class Item(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('price',
#         type=float,
#         required=True,
#         help='This field cannot be left blank!'
#         )
#
#     @jwt_required()
#     def get(self, name):
#         # for item in items:
#         #     if item['name'] == name:
#         #         return item
#         # use next to return first item found but will break if none found, hence the None at the end to catch error
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         return {'item': item}, 200 if item else 404
#
#
#     def post(self, name):
#         if next(filter(lambda x: x['name'] == name, items), None):
#             return {'message': "An item with name '{}' already exists.".format(name)}, 400
#
#         data = Item.parser.parse_args()
#
#         item = {'name':name, 'price': data['price']}
#         items.append(item)
#         return item, 201
#
#     def delete(self, name):
#         global items
#         items = list(filter(lambda x: x['name'] != name, items))
#         return {'message': 'Item deleted'}
#
#     def put (self, name):
#         data = Item.parser.parse_args()
#
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         if item is None:
#             item = {'name': name, 'price': data['price']}
#             items.append(item)
#         else:
#             item.update(data)
#         return item
#
# class ItemList(Resource):
#     def get(self):
#         return {'items':items}

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
