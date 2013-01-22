Eloi
====
(Regarding the name)[http://en.wikipedia.org/wiki/Eloi].

Get started
-----------

    git clone git@github.com:steinar/eloi.git
    cd eloi/
    mkvirtualenv --no-site-packages --distribute --python=python2.7 eloi
    workon eloi
    pip install -r requirements.txt

Create a database
-----------------

    python shell.py
    from booking.database import db
    db.create_all()
