from flask_restful import Resource
from flask import request, Response
from setup import ALLOWED_EXTENSIONS, jwt_key, qrCodeDetector
from db_models import User, Food, db, Product
import os
import json
import jwt
from datetime import datetime
import qrcode
from flask import send_file
from math import pi
from zxing import BarCodeReader
import cv2
import random

class ProductsImage(Resource):

    def get(self):
        token = request.headers.get('Authorization')
        token = token.replace("Bearer ", "")
        fname = jwt.decode(token, jwt_key, "HS256")["id"]
        return send_file(f'images/{fname}.jpg', mimetype='image/gif')

    def post(self):

        token = request.values["token"]
        file = request.files['products_image']
        fname = jwt.decode(token, jwt_key, "HS256")["id"]
        file.save(os.path.join("images", f"{fname}.jpg"))
        response = Response(
            json.dumps({
                "succes": "Successfully uploaded file."
                }),
            status=200, mimetype='application/json')

        return response

class GetToken(Resource):

    def get(self):
        new_user = User()
        db.session.add(new_user)
        db.session.commit()
        TOKEN = jwt.encode({'id': new_user.user_id,
                            'creation_date': str(datetime.today()),
                            'expiration_date': str(datetime.today())
                            }, jwt_key)
        #TOKEN = jwt.decode(TOKEN, jwt_key, "HS256")
        response = Response(
            json.dumps({'token': TOKEN}),
            status=202, mimetype='application/json')
        return response

class Products(Resource):

    def get(self):
        token = request.headers.get('Authorization')
        token = token.replace("Bearer ", "")
        id = jwt.decode(token, jwt_key, "HS256")["id"]
        args = request.args
        date = args["date"]
        date = datetime.fromtimestamp(int(date)/1000)
        date = date.replace(hour=0, minute=0, second=0,microsecond=0)
        products = Food.query.filter_by(user_id=id, date=date).all()
        products = [{
            "name": product.name,
            "weight": product.weight,
            "kcal": product.kcal,
            "carbs": product.carbs,
            "fats": product.fats,
            "protein": product.proteins
        } for product in products]
        response = Response(
            json.dumps({'data': products}),
            status=202, mimetype='application/json')
        return response

    def post(self):

        data = request.json
        token = data["token"]
        id = jwt.decode(token, jwt_key, "HS256")["id"]
        user = User.query.filter_by(user_id=id).first()
        food_data = data["food"]
        date = datetime.now()
        date = date.replace(hour=0, minute=0, second=0,microsecond=0)
        date = date
        for record in food_data:
            new_food = Food(
                int(user.user_id), record["name"], int(record["weight"]), int(record["kcal"]),
                int(record["carbs"]), int(record["fats"]),
                int(record["protein"]), date)
            db.session.add(new_food)
            db.session.commit()
        response = Response(
            json.dumps({
                "succes": "Successfully added products."
                }),
            status=200, mimetype='application/json')

        return response
  
class QR(Resource):

    def get(self):
        token = request.headers.get('Authorization')
        token = token.replace("Bearer ", "")
        id = jwt.decode(token, jwt_key, "HS256")["id"]
        qr = qrcode.make(token)
        fname = os.path.join("qr", f"{id}.jpg")
        qr.save(fname)
        return send_file(fname, mimetype='image/gif')

    def post(self):
        qr = request.files['qr']
        token = request.values["token"]
        try:
            id = jwt.decode(token, jwt_key, "HS256")["id"]
        except jwt.exceptions.DecodeError:
            id = random.randint(0,100)
        fname = os.path.join("qr", f"{id}.jpg")
        qr.save(fname)

        try:
            im = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
            blur = cv2.GaussianBlur(im, (5, 5), 0)
            ret, bw_im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            new_token = qrCodeDetector.detectAndDecode(bw_im)[0]
            id = jwt.decode(new_token, jwt_key, "HS256")["id"]
            response = Response(
                json.dumps({'token': new_token, 'id':id}),
                status=202, mimetype='application/json')
        except Exception as e:
            response = Response(
                json.dumps({'error': "Invalid QR"}),
                status=400, mimetype='application/json')
        os.remove(fname)
        
        return response

class Nutrition(Resource):
    
    def post(self):
        foods_measurements = request.json
        foods_data = []
        weight_to_nutrition = {}
        for food in foods_measurements:
            width1 = food["width"] * 2.15/2
            width2 = food["height"] * 2.15/2
            name = food["name"]
            product = Product.query.filter_by(name=name).first()
            if width1/width2 > 0.9 and width1/width2 < 1.1:
                height = width1 * product.proportions
            else:
                height = min(width1, width2)
            volume = 4/3 * pi * width1 * width2 * height
            weight = round(volume * product.density)
            weight_per_hundred = weight/100
            if name not in weight_to_nutrition:
                weight_to_nutrition[name] = {
                    "kcal": product.kcal,
                    "carbs": product.carbs,
                    "fats": product.fats,
                    "proteins": product.proteins
                }
            kcal = weight_per_hundred * product.kcal
            carbs = weight_per_hundred * product.carbs
            fats = weight_per_hundred * product.fats
            proteins = weight_per_hundred * product.proteins
            foods_data.append(
                {
                    "name": name,
                    "weight": int(weight),
                    "kcal": int(kcal),
                    "carbs": int(carbs),
                    "fats": int(fats),
                    "proteins": int(proteins)
                }
            )
        response = Response(
            json.dumps({'nutrition': foods_data, "weightToNutrition": weight_to_nutrition}),
            status=202, mimetype='application/json')
        return response
