from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
        )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
        )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            # return item
            # since Itemmodel.find_by_name has become an item object which contain dictionary(was moved into item model)
            return item.json()
        return {'message': 'Item not found'}, 404
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # use next to return first item found but will break if none found, hence the None at the end to catch error
        # removing below get method which get from local memory database
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404

    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None): # changing from local to database method
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # item = {'name':name, 'price': data['price']}
        # item is a dictionary and need to be item model object
        # since Item model has become an item object that contain dictionary (was moved into item model)
        # item = ItemModel(name, data['price'], data['store_id']) simplifying
        item = ItemModel(name, **data)

        # items.append(item) # changing from local to database method
        try:
            # ItemModel.insert(item) since it's item model object
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        # return item, 201 #item has turn into item model object
        return item.json(), 201

    def delete(self, name):
        # # global items
        # # items = list(filter(lambda x: x['name'] != name, items)) # changing from local to database method
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}
        # SQLalchemy changing to model to do deletion
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        # item = next(filter(lambda x: x['name'] == name, items), None) # changing from local to database method
        item = ItemModel.find_by_name(name)
        # # updated_item = {'name': name, 'price': data['price']}
        # # updated_item is a dictionary but item is a item model, changing it to item model
        # updated_item = ItemModel(name, data['price'])
        # SQLalchemy simplifying it by moving it down

        if item:
        # # changing from local to database method
        # #     item = {'name': name, 'price': data['price']}
        # #     items.append(item)
        # # else:
        # #     item.update(data)
        #     try:
        #         # ItemModel.insert(updated_item) # changing into item model method
        #         updated_item.insert()
        #     except:
        #         return {"message": "An error occured inserting the item."}, 500
        # else:
        #     try:
        #         # ItemModel.update(updated_item) # changing into item model method
        #         updated_item.update()
        #     except:
        #         return {"message": "An error occured updating the item."}, 500
        # # return updated_item # updated_item is item model object and we have to return dictionary
        # SQLalchemy simplifying
            # item = ItemModel(name, data['price'], data['store_id']) simplifying
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # # return {'items':items}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # connection.close()
        #
        # return {'items': items}
        # SQLalchemy simplifying
        # lambda method, more readable for other languages, return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # python only environment return{'items': [x.json() for x in ItemModel.query.all()]}
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
