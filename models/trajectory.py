from models.taxi import db


class Trajectory(db.Model):
    __tablename__ = "trajectories"

    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, db.ForeignKey("taxis.id"))
    date = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)