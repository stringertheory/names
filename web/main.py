import sys
import os

from flask import Flask, render_template, request, send_from_directory, json
from flask_frozen import Freezer
from flask.ext.assets import Environment, Bundle
from flask.ext.pymongo import PyMongo
from webassets.filter import get_filter

app = Flask(__name__)
app.config.from_object('settings')
freezer = Freezer(app)
assets = Environment(app)
mongo = PyMongo(app)

assets.register('js_all', Bundle(
    'js/main.js',
    'js/another.js',
    'js/rhyme.js',
    filters=('uglifyjs',),
    output='build/main.%(version)s.js',
    depends='js/*.js',
))

scss_path = os.path.join(app.static_folder, 'scss')
scss_filter = get_filter('scss', as_output=False, load_paths=[scss_path])
assets.register('css_all', Bundle(
    'scss/styles.scss',
    filters=(scss_filter,),
    output='build/main.%(version)s.css',
    depends='scss/*.scss',
))

@app.route('/')
def index():
    poems = mongo.db.poems.find(None, {'_id': True, 'title': True})
    return render_template('index.html', poems=poems)

@app.route('/poem/<_id>/')
def poem(_id):
    poem = mongo.db.poems.find_one({'_id': _id})
    return render_template('poem.html', poem=poem)

@app.route('/data/<_id>.json')
def data(_id):
    poem = mongo.db.poems.find_one(
        {'_id': _id},
        {'rhymes': True, 'analyzed': True},
    )
    return json.jsonify(poem)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'img/favicon.ico')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)
