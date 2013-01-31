import dateutil.parser
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
from booking.app import images
from booking.database import db

MODELS = []

def model(cls):
    if not hasattr(cls, '__tablename__'):
        raise Exception('%s does not have __tablename__ defined.' % cls.__name__)
    MODELS.append(cls)
    return cls


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

    def populate(self, **kwargs):
        return map(lambda (k,v): setattr(self, k, v), kwargs.items())

@model
class Location(UtilityMixIn, db.Model):
    __tablename__ = 'Location'

    def __init__(self, id=None, name='', slug='', type=0, description=u'', image_path='', price=0):
        self.populate(id=id, name=name, slug=slug, type=type, description=description, image_path=image_path, price=price)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.UnicodeText)
    slug = db.Column(db.String(120))
    type = db.Column(db.Integer)

order_slots = db.Table('order_slots', db.Model.metadata,
    db.Column('order_id', db.Integer, db.ForeignKey('Order.id')),
    db.Column('slot_id', db.Integer, db.ForeignKey('Slot.id'))
)

@model
class LocationImage(UtilityMixIn, db.Model):
    __tablename__ = 'LocationImage'

    def __init__(self, id=None, title='', description=u'', image_path='', location=None, location_id=None):
        self.populate(id=id, title=title, description=description, image_path=image_path, location=location, location_id=location_id)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.UnicodeText)
    image_path = db.Column(db.String(250))

    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'))
    location = db.relationship('Location', backref='images')

    @property
    def image_url(self):
        if not self.image_path:
            return None
        return images.url(self.image_path)


@model
class Slot(UtilityMixIn, db.Model):
    __tablename__ = 'Slot'

    def __init__(self, id=None, weekday=None, time_start=None, time_end=None, valid_from=None, valid_to=None, location=None, location_id=None):
        self.populate(id=id, weekday=weekday, time_start=time_start, valid_from=valid_from, valid_to=valid_to,
            location=location, location_id=location_id)

    @validates('valid_from', 'valid_to')
    def validate(self, name, value):
        """
        Location.valid_from.weekday() and Location.valid_to.weekday() must be the same as Location.weekday, that is,
        if the slot applies to a Tuesday both valid_to and valid_from must be Tuesdays.

        This is done to simplify database requests.
        """
        if isinstance(value, basestring):
            value = dateutil.parser.parse(value)

        if value.weekday() == self.weekday:
            raise ValueError('%s does not match with weekday (%s)' % (name, self.weekday))

        return value

    id = db.Column(db.Integer, primary_key=True)

    weekday = db.Column(db.Integer) # Make required or default 0
    time_start = db.Column(db.Time) # Make required
    time_end = db.Column(db.Time) # Make required

    price = db.Column(db.Integer)

    valid_from = db.Column(db.Date) # Make required
    valid_to = db.Column(db.Date) # Make required

    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'))
    location = db.relationship('Location', backref='slots')

@model
class Order(UtilityMixIn, db.Model):
    __tablename__ = 'Order'

    def __init__(self, id=None, date_start=None, date_end=None, name='', email='', phone='', comment='', paid=False, slots=None):
        self.populate(id=id, date_start=date_start, date_end=date_end, name=name, email=email, phone=phone, comment=comment,
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
    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'))
    location = db.relationship('Location', backref='orders')


# If any of the tables are missing, do db.create_all
if any([not db.engine.dialect.has_table(db.engine.connect(), cls.__tablename__) for cls in MODELS]):
    db.create_all()
