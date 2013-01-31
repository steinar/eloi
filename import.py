import os
import sys
import yaml
from booking.app import app
from booking.database import db
from booking.models import MODELS, TABLES
from booking.settings import SERVER_PORT
from booking import views



def import_item(model, item):
    return

def import_file(filename):
    models = dict(map(lambda x: (x.__tablename__, x), MODELS))
    tables = dict(map(lambda x: (x.name, x), TABLES))
    data = yaml.load(open(filename, 'r'))

    instances = []
    table_entries = []
    errors = []

    for (type_name, items) in data.items():
        try:
            instances.extend([
                models[type_name](**item)
                for item in items
                if type_name in models
            ])
            table_entries.extend([
                tables[type_name].insert().values(**item)
                for item in items
                if type_name in tables
            ])
        except Exception, e:
            errors.append((type_name, e, item))

    if errors:
        print "The following errors occurred:"
        for (type_name, msg, item) in errors:
            print type_name
            print msg
            print item
            print

        return

    for item in instances:
        print "Saving", item
        item.save(commit=False)

    for item in table_entries:
        print "Inserting into table", item.table.name
        db.session.execute(item)

    db.session.commit()

    print "All done. =)"


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        raise Exception("First argument should be a file path")

    import_file(filename)