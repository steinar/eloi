import yaml

from flask import request
from flask.templating import render_template

from booking.app import app


@app.route('/')
def locations():
    data = yaml.load(file('base.yaml', 'r'))
    return render_template('location.html', locations=data['Location'])


@app.route('/location/<location_slug>/')
def location(location_slug):
    weeks = request.args.get('weeks', '')
    weeks = weeks and weeks.split('-') or []
    return render_template('slots.html', location_slug=location_slug, weeks=weeks)
