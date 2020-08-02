from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    @jwt_required()
    def get(self):
        id_user = current_identity.id
        store = StoreModel()
        result = store.get_store_by_id_user(id_user)
        if result:
            return store.json()
        return {'message': 'Store not found'}, 404
    
    @jwt_required()
    def post(self):
        id_user = current_identity.id
        data = Store.parser.parse_args()
        if StoreModel.get_store_by_name(data["store_name"]):
            return {'message': "A store with name '{}' already exists.".format(data["store_name"])}, 400
        
        if StoreModel.get_store_by_id_user(id_user):
            return {'message': "This user already has store."}, 403

        store = StoreModel()
        try:
            result = store.insert_store(data["store_name"], id_user)
            return {"message" : "New store already added with ID : {}".format(result)}, 201
        except:
            return {"message": "An error occurred creating the store."}, 500
