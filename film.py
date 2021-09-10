from flask import Flask,render_template, jsonify, request , make_response
from firebase_admin import credentials, firestore, initialize_app


import os

app = Flask(__name__)
port = int(os.environ.get("PORT",5000))

cred = credentials.Certificate('Data/key.json')
default_app = initialize_app(cred)
db = firestore.client()
doc_ref = db.collection('bddfilms').document('ZaE2fwAxJfzrq0PdWFPw')

emp_ref = db.collection('bddfilms')
docs =emp_ref.stream()

@app.route('/')
def index():
	return '/films to see all films'

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection 
       
    """
    try:
        id = request.json['id']
        doc_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        all_todos : Return all documents
    """
    try:

        docs =emp_ref.stream()
        all_todos = [doc.to_dict() for doc in docs]
        return jsonify(all_todos), 200

    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection
    """
    try:
        id = request.json['id']
        doc_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        doc_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}),404)

if __name__ == "__main__":        
    app.run(debug=True,host='127.0.0.1',port = port) #local
	#app.run(host = "0.0.0.0", port = port, debug=True) #container              
