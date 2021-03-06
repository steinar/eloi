import calendar
from datetime import date, timedelta
from urllib import urlencode

from booking.app import images
from booking.models import Location, Slot, LocationImage


def get_locations():
    return Location.all()


def get_slots(location, for_date):
    """
    Get all valid slots for a location for a given date
    """
    assert isinstance(location, Location)
    assert isinstance(for_date, date)

    return Slot.query.filter_by(location=location).filter_by(weekday=for_date.weekday())\
        .filter(Slot.valid_from <= for_date).filter(Slot.valid_to >= for_date)\
        .order_by('time_start').all()


def get_slots_week(location, date_in_week):
    """
    Return all valid slots for a week. The date may be any day of the week (e.g. datetime.now())
    """
    assert isinstance(location, Location)
    assert isinstance(date_in_week, date)

    first_day = date_in_week - timedelta(days=date_in_week.weekday())
    last_day = first_day + timedelta(days=6)

    # Single query which returns all slots which are valid at some point during the week in question
    all_possible_slots = Slot.query.filter_by(location=location)\
        .filter(Slot.valid_from <= last_day).filter(Slot.valid_to >= first_day)\
        .order_by('weekday', 'time_start').all()

    return all_possible_slots


def get_slots_week_as_dict(location, date_in_week):
    """
    Put slots of a week in 7 buckets, one for each day.
    """
    weekday_dict = dict(zip(range(7), map(lambda i: [], range(7))))
    for slot in get_slots_week(location, date_in_week):
        weekday_dict[slot.weekday].append(slot)
    return weekday_dict


def create_location_image(location, image_storage, title='', description=''):
    """
    Returns a LocationImage instance. Note that it has not been saved.
    image_storage is typically request.files['image']
    """
    saved_path = images.save(image_storage)
    return LocationImage(title, description, saved_path, location)


def get_month_link(location, months_range, current_date_range):
    today = date.today()
    year = today.year + (today.month + months_range) / 12
    month = (today.month + months_range) % 12
    if month == 0:
        month = 12
        year -= 1

    weekday, days = calendar.monthrange(year, month)
    first_day = date(year, month, 1)
    last_day = date(year, month, days)
    date_range = '%s:%s' % (first_day.isoformat(), last_day.isoformat())
    url_params = urlencode({'date_range': date_range})
    link = {
        'href': '/location/%s/?%s' % (location, url_params),
        'title': first_day.strftime('%B %Y'),
        'active': date_range == current_date_range
    }
    return link
