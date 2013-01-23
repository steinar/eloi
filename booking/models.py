from sqlalchemy.exc import OperationalError
from booking.database import db

class UtilityMixIn(object):
    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self):
        if not self.validate():
            raise RuntimeError('Instance %s is invalid' % self)

        try:
            db.session.add(self)
            db.session.commit()
        except OperationalError, e:
            db.session.rollback()
            raise RuntimeError(e)

    def validate(self):
        return True

    def populate(self, **kwargs):
        return map(lambda (k,v): setattr(self, k, v), kwargs.items())


class Location(UtilityMixIn, db.Model):
    def __init__(self, name='', slug='', type=0, description='', image_path=''):
        self.populate(name=name, slug=slug, type=type, description=description, image_path=image_path)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.UnicodeText)
    image_path = db.Column(db.String(250))
    slug = db.Column(db.String(120))
    type = db.Column(db.Integer)


order_slots = db.Table('order_slots', db.Model.metadata,
    db.Column('order_id', db.Integer, db.ForeignKey('Order.id')),
    db.Column('slot_id', db.Integer, db.ForeignKey('Slot.id'))
)


class Slot(UtilityMixIn, db.Model):
    __tablename__ = 'Slot'

    def __init__(self, weekday=None, time_start=None, time_end=None, valid_from=None, valid_to=None, location=None):
        self.populate(weekday=weekday, time_start=time_start, valid_from=valid_from, valid_to=valid_to,
            location=location)

    def validate(self):
        """
        Location.valid_from.weekday() and Location.valid_to.weekday() must be the same as Location.weekday, that is,
        if the slot applies to a Tuesday both valid_to and valid_from must be Tuesdays.

        This is done to simplify database requests.
        """
        return ((not self.valid_from or self.valid_from.weekday() == self.weekday) and
               (not self.valid_to or self.valid_to.weekday() == self.weekday))

    id = db.Column(db.Integer, primary_key=True)

    weekday = db.Column(db.Integer)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)

    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='slots')


class Order(UtilityMixIn, db.Model):
    __tablename__ = 'Order'

    def __init__(self, date_start=None, date_end=None, name='', email='', phone='', comment='', paid=False, slots=None):
        self.populate(date_start=date_start, date_end=date_end, name=name, email=email, phone=phone, comment=comment,
        paid=paid, slots=slots)
        self.location = slots[0].location if slots else None

    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.Date())
    date_end = db.Column(db.Date())

    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    comment = db.Column(db.UnicodeText)

    paid = db.Column(db.Boolean)

    slots = db.relationship('Slot', secondary=order_slots, backref='orders')

    # Note: Just for convenience. Set automatically based on slots.
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='orders')


