from sqlalchemy.exc import OperationalError
from booking.database import db

class UtilityMixIn(object):
    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except OperationalError, e:
            db.session.rollback()
            raise RuntimeError(e)


class Location(UtilityMixIn, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    type = db.Column(db.Integer)

class Booking(UtilityMixIn, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(120))

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='locations', lazy='immediate', primaryjoin='Location.id==Booking.location_id')
