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


## Kröfur

Sjá núverandi síðu <http://fbjork.is/Forsida/Leigaasolum>

### Forsíða:

Listi af sölum 6 stykki:

- Dans- og veislusalur
- Litla Björk
- Afmælissalur
- Andrasalur
- Mínervusalur
- Bjarkarsalur

Almenn lýsing á sölum

### Salur

Model:

- Titill
- Stutt lýsing
- Mynd (kanski fleiri en ein)
- Ítarleg lýsing

---

### Kröfur

- Það þarf að vera hægt að setja upp á hvaða tímum salirnir eru lausir.
- Umsjónarmaður þarf að fá yfirlit yfir allar pantanir
- Umsjónarmaður getur staðfest greiðslu og þá er ekki lengur hægt að panta.
-





