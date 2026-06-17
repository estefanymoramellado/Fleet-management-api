from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Taxi(db.Model):
    __tablename__ = "taxis"

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String)