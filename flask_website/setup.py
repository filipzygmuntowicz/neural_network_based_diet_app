from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)
with open("jwt_key.txt", "r") as f:
    jwt_key = f.read()
qrCodeDetector = cv2.QRCodeDetector()