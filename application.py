import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from models import *
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/", methods = ["POST", "GET"])
def index():
    form = request.form

    if request.method == 'POST':
        display_name = form.get('name')
        password = form.get('password')
        u = User(name=name, password=password)

        print(display_name)
        print(password)

        u.add_user()
        
    return render_template("index.html")

if __name__ == ' __main__':
    #app.debug = True
    app.run()