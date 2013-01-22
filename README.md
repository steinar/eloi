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
- Litla Björk (LB)
- Afmælissalur (AS)
- Andrasalur
- Mínervusalur
- Bjarkarsalur

Almenn lýsing á sölum

## Model

Salur
-----------
    Titill 
    Stutt lýsing
    Mynd (kanski fleiri en ein)
    Ítarleg lýsing

Pöntun
-----------
     Nafn
     Tölvupóstur
     Sími
     Greitt


### Almennar kröfur

## Almennur notandi
- Getur séð yfirlit yfir alla sali
- Getur skoðað sal nánar (fær nánari lýsingu og reglur)
- Getur pantað sal (umsjónarmaður setur upp hvaða tímar eru lausir). Til að byrja með er aðeins hægt Litlu Björk (LB) og Afmælissal (AS). 
- Getur sent fyrirspurn út af öðrum sölum en LB og AS
- Fær upplýsingar um greiðslu og reglur sem gilda um sali við pöntun
- 

## Umsjónarmaður
- Umsjónarmaður getu sett upp á hvaða tímum salirnir eru lausir.
- Umsjónarmaður þarf að fá yfirlit yfir allar pantanir
- Umsjónarmaður getur staðfest greiðslu og þá er ekki lengur hægt að panta.
- Umsjónarmaður getur eytt út pöntun
- Umsjónarmaður getur breytt lýsingu á sölum

## Auka kröfur
- Gera pantanir aðgengilegar í gegnum ical
- Geta pantað aðra sali en Litla Björk og Veislusal
- 
