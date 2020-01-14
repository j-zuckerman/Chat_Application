import os

from flask import Flask, render_template, request


from models import *

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nwsfdmosrnutwy:df73ed703a73a36118363ad6669abc0727cdccfa84676162718a492d95290a8a@ec2-174-129-32-200.compute-1.amazonaws.com:5432/dcvopec8rdaflu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  
db.init_app(app)

def main():
      
    db.create_all()

if __name__ == "__main__":
     
    with app.app_context():
        main()