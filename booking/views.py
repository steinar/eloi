from dateutil.parser import parse
from random import randrange
import yaml

from flask import request
from flask.templating import render_template

from booking.app import app
from booking.utils import get_month_link


def slot():
    status = randrange(2) == 1 and 'booked' or 'available'
    return {'class': status,
            'href': '#',
            'time': '18:00 - 21:00'}


@app.route('/')
def locations():
    data = yaml.load(file('base.yaml', 'r'))
    return render_template('location.html', locations=data['Location'])


@app.route('/location/<location_slug>/')
def location(location_slug):
    date_range_params = request.args.get('date_range', [])

    if date_range_params:
        date_range = [parse(i).date() for i in date_range_params.split(':')]

    day = lambda d: {'title': d}

    week = lambda x: [day(d) for d in ('Monday', 'Tuesday', 'Wednesday',
                                       'Thursday', 'Friday', 'Saturday',
                                       'Sunday')]
    weeks = [week('') for i in range(4)]

    for i in range(len(weeks)):
        for j in range(len(weeks[i])):
            slots = [slot() for k in range(randrange(3))]
            weeks[i][j].update({'slots': slots})

    ctx = {
        'location_slug': location_slug,
        'month_links': [get_month_link(location_slug, i, date_range_params)
                        for i in range(12)],
        'weeks': weeks
    }

    return render_template('slots.html', **ctx)
