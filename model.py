from flask_sqlalchemy import SQLAlchemy
from app import app


db=SQLAlchemy(app)


class TypeDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    serial_number_mask = db.Column(db.String(100),  nullable=False)
    device_id =  db.relationship('Device', backref='type_device', lazy='dynamic')

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(20), unique=True, nullable=False)
    type_device_id = db.Column(db.Integer, db.ForeignKey('type_device.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

