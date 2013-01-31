import os
from booking.app import app
from booking.settings import SERVER_PORT
from booking import views

if __name__ == "__main__":
    port = int(os.environ.get('PORT', SERVER_PORT))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
