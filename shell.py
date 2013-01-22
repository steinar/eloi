import sys

from werkzeug import script

from app import app

def make_shell():
    return dict(app=app,)

if __name__ == "__main__":
    script.make_shell(make_shell, use_ipython=True)()