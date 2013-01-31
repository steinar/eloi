from flask import Flask
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from booking import settings

app = Flask(__name__)


# Images
app.config['UPLOADS_DEFAULT_DEST'] = settings.UPLOADS_DEFAULT_DEST
app.config['UPLOADS_DEFAULT_URL'] = settings.UPLOADS_DEFAULT_URL
images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))
