import sys
import yaml
from booking.database import db
from booking.models import MODELS, TABLES


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
                (models[type_name], item)
                for item in items
                if type_name in models
            ])
            table_entries.extend([
                (tables[type_name], item)
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

    for model,kwargs in instances:
        print "Constructing", model
        item, created = model.get_or_create(**kwargs)
        print (created and "Creating" or "Updating"), item
        item.save(commit=False)

    for table,kwargs in table_entries:
        print "Checking", table.name
        select = table.select()
        for k,v in kwargs.items():
            select = select.where(getattr(table.c, k) == v)

        if not db.session.execute(select).first():
            print "Inserting into", table.name
            db.session.execute(table.insert().values(**kwargs))
        else:
            print "Found and skipping in", table.name


    db.session.commit()

    print "All done. =)"


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        raise Exception("First argument should be a file path")

    import_file(filename)