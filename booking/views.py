import yaml
from flask.templating import render_template

from booking.app import app


@app.route('/')
def locations():
    data = yaml.load(file('base.yaml', 'r'))
    return render_template('location.html', locations=data['Locations'])
