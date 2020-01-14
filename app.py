import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from models import *
from flask_heroku import Heroku


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nwsfdmosrnutwy:df73ed703a73a36118363ad6669abc0727cdccfa84676162718a492d95290a8a@ec2-174-129-32-200.compute-1.amazonaws.com:5432/dcvopec8rdaflu'
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
        u = User(name=display_name, password=password)

        print(display_name)
        print(password)

        u.add_user()
        
    return render_template("index.html")

if __name__ == ' __main__':
    #app.debug = True
    app.run()