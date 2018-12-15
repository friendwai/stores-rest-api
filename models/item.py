from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query,(name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     # return {'item': {'name': row[0], 'price': row[1]}}
        #     # because this is a class method which call on ItemModel init method, row then call into it's arguement name and price
        #     # use *row argument unpacking which pass each in row argument into each element
        #     return cls(*row)
        # simplifying using SQLalchemy
        return cls.query.filter_by(name=name).first()

    # @classmethod
    # def insert(cls, item):
    # since this had been move into a item model which handle item, it make sense to use self
    # instead item from previous resources package
    # def insert(self):
    # SQLalchemy session retrieve data update and insert hence  changing name
    def save_to_db(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?, ?)"
        # # cursor.execute(query, (item.['name'], item.['price'])
        # # changing to self now because self is an object not dictionary
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()
        # simplifying using SQLalchemy
        db.session.add(self)
        db.session.commit()

    # @classmethod
    # def update(cls, item):
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE items SET price=? WHERE name=?"
    #     # cursor.execute(query, (item.['name'], item.['price'])
    #     # changing to self now because self is an object not dictionary
    #     cursor.execute(query, (self.price, self.name))
    #
    #     connection.commit()
    #     connection.close()
    # save_to_db doing insert and update hence no longer userful
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
