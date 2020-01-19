import os

from flask import Flask, url_for, session, redirect, render_template, request, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
from models import *
from flask_heroku import Heroku


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nwsfdmosrnutwy:df73ed703a73a36118363ad6669abc0727cdccfa84676162718a492d95290a8a@ec2-174-129-32-200.compute-1.amazonaws.com:5432/dcvopec8rdaflu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    return render_template("index.html")
  

@app.route("/register", methods=['POST', 'GET'])
def register():
    
    form = request.form

    if request.method == 'POST':
        display_name = form.get('name')
        password = form.get('password')
        u = User(name=display_name, password=password)

        print(display_name)
        print(password)

        u.add_user()
        return redirect(url_for("channels"))
        
    return render_template("register.html")

@app.route("/login", methods =['GET', 'POST'])
def login():
    form = request.form

    if request.method == 'POST':
        name = form.get('name')
        password = form.get('password')

        print(name)
        print(password)
        u = User.query.filter_by(name=name).first()
        print(u)
        if u is None or u.password != password:
            return render_template("error.html", message="Incorrect login information")
        else:
            session["user"] = u
            return redirect(url_for("channels"))
        
    return render_template("login.html")

@app.route("/channels", methods=['GET', 'POST'])
def channels():
    
    channels = Channel.query.all()


    return render_template("channels.html", channels = channels)

@app.route("/channel/<string:id>")
def channel(id):
    user_names = []
    channel = Channel.query.get(id)
    
    for message in channel.messages:
        user_name = User.query.filter_by( id = message.user_id).first().name
        user_names.append(user_name)
    
    print(user_names)
    
    return render_template("messages.html", channel=channel, user_names = user_names)

@socketio.on("create channel")
def socket_create_channel(data):
    channel = Channel.query.filter_by(name=data['name']).first()
    if channel == None:
        c = Channel(name=data['name'])
        c = c.add_channel()
        data['id'] = c.id
        emit("channel created", data, broadcast=True)    

@socketio.on("send message")
def socket_send_message(data):
    channel_id = data["id"]
    message = data["message"]
    channel = Channel.query.get(channel_id)
    channel.add_message(message, session['user'].id)
    data['user_id'] = session['user'].id
    u =  User.query.filter_by(id = data['user_id']).first()
    data['name'] = u.name
    emit("message received", data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)