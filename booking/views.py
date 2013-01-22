from flask.templating import render_template

from booking.app import app


@app.route('/')
def locations():

    # Test data, will be replaced by data from the database
    locations = [{
        'title': u'Dans og veislusalur',
        'img': 'http://fbjork.is/thumb.php?file=/files/138-0.jpg&size=200x150',
        'description': 'Description'
    }, {
        'title': u'Dans og veislusalur',
        'img': 'http://fbjork.is/thumb.php?file=/files/138-0.jpg&size=200x150',
        'description': 'Description'
    }]
    return render_template('location.html', locations=locations)
