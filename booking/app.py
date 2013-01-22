from flask import Flask
from settings import SERVER_PORT


app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=SERVER_PORT)