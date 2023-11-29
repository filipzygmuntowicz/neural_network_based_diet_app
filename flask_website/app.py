from db_models import db, app, api, Product
from api_endpoints import ProductsImage, GetToken, Products, QR, Nutrition
from routing import app
import json

with app.app_context():
    db.create_all()

def update_products_database():
    with open('products_table.json', 'r') as file:
        with app.app_context():
            products_data = json.load(file)
            for product in products_data:
                name = product["name"]
                density = product["density"]
                proportions= product["proportions"]
                kcal = product["kcal"]
                carbs = product["carbs"]
                fats = product["fats"]
                proteins = product["proteins"]
                new_product = Product(name, density, proportions, kcal, carbs, fats, proteins)
                db.session.add(new_product)
            db.session.commit()


api.add_resource(ProductsImage, "/api/products_image")
api.add_resource(GetToken, "/api/get_token")
api.add_resource(Products, "/api/products")
api.add_resource(QR, "/api/qr")
api.add_resource(Nutrition, "/api/nutrition")
if __name__ == '__main__':
    update_products_database()
    app.run()
