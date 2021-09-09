from flask import Flask,render_template, jsonify, make_response,abort

import json
import os, sys


app = Flask(__name__)
port = int(os.environ.get("PORT",5000))
films = json.load(open("Data/films.json"))

@app.route('/')
def index():
	return '/films to see all films'

@app.route('/films',methods=['GET'])
def get_films():
	return jsonify({"films":films})

@app.route('/films/<string:title>',methods=['GET'])
def get_film_title(title):
	film = [film for film in films if film["Title"] == title ]
	if len(film) ==0:
		abort(404,"film with title::{} does not exit".format(title))
	return render_template('film.html', title="film", jsonfile=json.dumps({"films":film}))

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}),404)

if __name__ == "__main__":        
    # app.run(debug=True,host='127.0.0.1',port = port) 
	app.run(host = "0.0.0.0", port = port, debug=True)                
