# db.py

from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    app.config["MONGO_URI"] = "mongodb+srv://hassanmuzaffar439:xRgY3in5QCOr5Rzk@cluster0.b5ien.mongodb.net/petfeeder?retryWrites=true&w=majority&appName=Cluster0"
    mongo.init_app(app)
