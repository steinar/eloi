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
    slug = db.Column(db.String(120))
    type = db.Column(db.Integer)


order_slots = db.Table('order_slots', db.Model.metadata,
    db.Column('order_id', db.Integer, db.ForeignKey('Order.id')),
    db.Column('slot_id', db.Integer, db.ForeignKey('Slot.id'))
)


class Slot(UtilityMixIn, db.Model):
    __tablename__ = 'Slot'

    id = db.Column(db.Integer, primary_key=True)

    weekday = db.Column(db.Integer)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)

    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='locations', lazy='immediate', primaryjoin='Location.id==Slot.location_id')


class Order(UtilityMixIn, db.Model):
    __tablename__ = 'Order'

    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.Date())
    date_end = db.Column(db.Date())

    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    comment = db.Column(db.UnicodeText)

    paid = db.Column(db.Boolean)

    slots = db.relationship('Slot', secondary=order_slots, backref='orders')


