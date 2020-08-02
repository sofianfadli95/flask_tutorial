from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel, ItemList
from models.store import StoreModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Every item needs a name."
                        )
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help="Every item needs a price."
                        )
    parser.add_argument('descriptions',
                        type=str,
                        required=True,
                        help="Every item needs a descriptions."
                        )
    
    @jwt_required()
    def get(self, id_item):
        item = ItemModel()
        result = ItemModel.get_item_by_id(id_item)
        if result:
            return item.json()
        return {'message': 'Item not found'}, 404
    
    @jwt_required()
    def post(self, id_item):
        id_user = current_identity.id
        store = StoreModel()
        store.get_store_by_id_user(id_user)
        data = Item.parser.parse_args()
        # print(data)
        data['id_store'] = store.id_store

        # if ItemModel.get_item_by_name(data['name']):
        #    return {'message': "An item with name '{}' already exists.".format(data['name'])}, 400
        
        item = ItemModel()

        try:
            result = item.insert_item(**data)
        except:
            return {"message": "An error occurred when inserting the item."}, 500

        return {"message" : "New item already added  with ID : {}".format(result)}, 201
    
    @jwt_required()
    def delete(self, id_item):
        id_user = current_identity.id
        store = StoreModel()
        store.get_store_by_id_user(id_user)
        item = ItemModel.get_item_by_id(id_item)
        if item:
            ItemModel.delete_item(id_item, store.id_store)
            return {'message': 'Item has been deleted.'}
        return {'message': 'Item not found.'}, 404
    
    @jwt_required()
    def put(self, id_item):
        id_user = current_identity.id
        store = StoreModel()
        store.get_store_by_id_user(id_user)
        data = Item.parser.parse_args()
        item = ItemModel()
        result = item.get_item_by_id(id_item)

        if result:
            item.update_item(id_item, data['name'], data['price'], data['descriptions'], store.id_store)
            return {"message" : "Item with ID : {} has been updated".format(id_item)}
        else:
            id_item = ItemModel.insert_item(**data)
            return {"message" : "New item already added with ID : {}".format(id_item)}



class ItemsInStore(Resource):
    @jwt_required()
    def get(self):
        id_user = current_identity.id
        store = StoreModel()
        store.get_store_by_id_user(id_user)
        items = ItemList()
        results = items.get_items_by_id_store(store.id_store)
        if results:
            return items.json()
        return {'message': "There is no items in this store"}
