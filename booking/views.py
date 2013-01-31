import yaml

from flask import request
from flask.templating import render_template

from booking.app import app
from booking.utils import get_month_link


@app.route('/')
def locations():
    data = yaml.load(file('base.yaml', 'r'))
    return render_template('location.html', locations=data['Location'])


@app.route('/location/<location_slug>/')
def location(location_slug):
    date_range = [request.args.get('date_from', ''),
                  request.args.get('date_to', '')]
    ctx = {'location_slug': location_slug,
           'date_range': date_range,
           'month_links': [get_month_link(location_slug, i) for i in range(12)]}

    return render_template('slots.html', **ctx)
