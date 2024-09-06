from flask import (Flask, redirect, render_template, request,send_from_directory, url_for)
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import random

load_dotenv()
app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
socketio = SocketIO(app)

@app.route('/')
def index():
   print('Request for index page received.')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'images/mylogo.png', mimetype='image/vnd.microsoft.icon')

@socketio.on('request stimuli')
def send_stims():
   #make a list of some weird animals (and some fake ones)
   animals=[{'name': 'mastodon', 'status': 'realAnimal'}, {'name': 'hutia', 'status': 'realAnimal'}, {'name': 'dodo', 'status': 'realAnimal'}, {'name': 'hellbender', 'status': 'realAnimal'}, {'name': 'bluebuck', 'status': 'realAnimal'}, {'name': 'fossa', 'status': 'realAnimal'}, {'name': 'tarpan', 'status': 'realAnimal'}, {'name': 'thylacine', 'status': 'realAnimal'}, {'name': 'baiji', 'status': 'realAnimal'}, {'name': 'saola', 'status': 'realAnimal'}, {'name': 'vaquita', 'status': 'realAnimal'}, {'name': 'indris', 'status': 'realAnimal'}, {'name': 'coua', 'status': 'realAnimal'}, {'name': 'sifakas', 'status': 'realAnimal'}, {'name': 'pochard', 'status': 'realAnimal'}, {'name': 'tenerec','status':'realAnimal'},{'name':'aurochs', 'status': 'realAnimal'}, {'name': 'kouprey', 'status': 'realAnimal'}, {'name': 'asbino', 'status': 'notAnimal'}, {'name': 'babblo', 'status': 'notAnimal'}, {'name': 'sormy', 'status': 'notAnimal'}, {'name': 'dorker', 'status': 'notAnimal'}, {'name': 'wooxen', 'status': 'notAnimal'}, {'name': 'moozy', 'status': 'notAnimal'}, {'name': 'hokegiper', 'status': 'notAnimal'}, {'name': 'willew', 'status': 'notAnimal'}, {'name': 'phorl', 'status': 'notAnimal'}, {'name': 'smoop', 'status': 'notAnimal'}, {'name': 'glistle', 'status': 'notAnimal'}, {'name': 'dreat', 'status': 'notAnimal'}, {'name': 'waxgork', 'status': 'notAnimal'}, {'name': 'redsnop', 'status': 'notAnimal'}, {'name': 'mattle', 'status': 'notAnimal'}, {'name': 'carmth', 'status': 'notAnimal'}, {'name': 'sarlock', 'status': 'notAnimal'}, {'name': 'pagtail', 'status': 'notAnimal'}]
   #shuffle it into a random order
   random.shuffle(animals)
   #send it back to the front-end/client
   emit('randomized stimuli',{"data":animals})

@socketio.on('check human')
def check_human(message):
   print("Check human message:",message)
   isHuman=False
   humananswer=message["data"]
   #take out any spaces and make lowercase
   finalanswer=humananswer.rstrip().lower()
   validanswers=["enter three","enter 3","enterthree","enter3"]
   if finalanswer in validanswers:
      isHuman=True
   emit('human verified',{"data":isHuman})

@socketio.on('store responses')
def store_stims(message):
   responses=message["data"]
   #here is where we would send the responses to a database

@socketio.on('connect')
def test_connection():
   print("The front end wants to connect. What say you?")
   emit('connection confirmation',{"data":"Your server says hello!"})


if __name__ == '__main__':
   app.run()
