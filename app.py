from flask import Flask, session, request, render_template, jsonify
from random import randint
from controllers.AuthController import AuthController
from controllers.WatchTitleController import WatchTitleController
from controllers.SeasonController import SeasonController
from models.WatchTitle import WatchTitle
import os
import requests

app = Flask(__name__,
            static_folder='./dist/static',
            template_folder='./dist')
app.secret_key = os.environ.get('ANTRACKER_SECRET_KEY')
watch_title_controller = WatchTitleController()
auth_controller = AuthController()
season_controller = SeasonController()


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template('index.html')

@app.route('/auth/register', methods=['POST'])
def auth():
    return auth_controller.register(request.json)

@app.route('/auth/login', methods=['POST'])
def login():
    return auth_controller.login(request.json)

@app.route('/auth/verify', methods=['POST'])
def verify():
    if 'username' in session:
        return auth_controller.verify()
    else:
        return jsonify({'result': 'Not logged in'})

@app.route('/seasons/get', methods=['POST'])
def get_seasons():
    #return jsonify(Test.test_season_data)
    result = season_controller.getUserSeasons(request.json)
    if not result:
        return jsonify({'result': 'Failed'})
    return result

@app.route('/watchtitle/add', methods=['POST'])
def add_title():
    #return jsonify(request.json)
    watchtitle = WatchTitle(request.json)
    return watch_title_controller.addWatchTitle(watchtitle)

@app.route('/watchtitle/delete', methods=['POST'])
def delete_title():
    #return jsonify(request.json)
    return watch_title_controller.deleteWatchTitle(request.json)

@app.route('/watchtitle/get', methods=['POST'])
def get_title():
    #return jsonify(Test.test_item_data)
    return watch_title_controller.getWatchTitle(request.json)

@app.route('/watchtitle/update', methods=['POST'])
def update_title():
    #return jsonify(request.json)
    return watch_title_controller.updateWatchTitle(request.json)
