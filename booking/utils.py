from datetime import date, timedelta
from booking.models import Location, Slot

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

    first_day = date_in_week-timedelta(days=date_in_week.weekday())
    last_day = first_day+timedelta(days=6)

    # Single query which returns all slots which are valid at some point during the week in question
    all_possible_slots = Slot.query.filter_by(location=location)\
        .filter(Slot.valid_from <= last_day).filter(Slot.valid_to >= first_day)\
        .order_by('weekday', 'time_start').all()

    return all_possible_slots


def get_slots_week_as_dict(location, date_in_week):
    """
    Put slots of a week in 7 buckets, one for each day.
    """
    pairs = map(lambda slot: (slot.weekday, slot), get_slots_week(location, date_in_week))
    weekday_dict = dict(zip(range(7), map(lambda i: [], range(7))))
    for (weekday, slot) in pairs:
        weekday_dict[weekday].append(slot)
    return weekday_dict










