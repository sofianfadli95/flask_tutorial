from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsInStore
from resources.store import Store

app = Flask(__name__)
app.secret_key = 'mysecretkey'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store')
api.add_resource(Item, '/item/<string:id_item>')
api.add_resource(ItemsInStore, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
