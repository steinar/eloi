import os
from booking.app import app
from booking import views

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8100))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
