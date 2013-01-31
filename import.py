import os
import sys
import yaml
from booking.app import app
from booking.models import MODELS
from booking.settings import SERVER_PORT
from booking import views



def import_item(model, item):
    return

def import_file(filename):
    models = dict(map(lambda x: (x.__tablename__, x), MODELS))
    data = yaml.load(open(filename, 'r'))

    instances = []
    errors = []

    for (model_name, items) in data.items():
        try:
            instances.extend([models[model_name](**item) for item in items])
        except Exception, e:
            errors.append((model_name, e, item))

    if errors:
        print "The following errors occurred:"
        for (model_name, msg, item) in errors:
            print model_name
            print msg
            print item
            print

        return

    for item in instances:
        print "Saving", item
        item.save()

    print "All done. =)"


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        raise Exception("First argument should be a file path")

    import_file(filename)