from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity

app = Flask(__name__)

api = Api(app)

app.secret_key ='amit'

jwt = JWT(app,authenticate,identity)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='Price is required field')

    @jwt_required()
    def get(self, name):
        return list(filter(lambda i: i['name'] == name, items))

    @jwt_required()
    def post(self, name):

        # item_data = request.get_json()

        item_data = Item.parser.parse_args()

        if name is not None:
            item = next(filter(lambda i: i['name'] == name, items), None)
            if item is None:
                item = {'name': name, 'price': item_data['price']}
                items.append(item)
                return item, 201
            else:
                return {'error': 'Item already Exists'}, 400
        else:
            return {'error': 'Item Name is required'}, 400

    @jwt_required()
    def delete(self, name):
        global items
        item = next(filter(lambda i: i['name'] == name, items), None)
        if item is not None:
            items = list(filter(lambda x: x['name'] != name, items))
            return {'message': 'Item {0} is deleted'.format(name)}, 203
        else:
            return {'error': 'Item Not found '}, 400

    @jwt_required()
    def put(self, name):

        item_data = Item.parser.parse_args()

        item = next(filter(lambda i: i['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': item_data['price']}
            items.append(item)
            return items, 203
        else:
            item.update({'price': item_data['price']})
            return item, 200


class ItemList(Resource):

    @jwt_required()
    def get(self):
        return items, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/itemList/')

app.run(port=5000)
