from flask import jsonify, request
from controller import Controller
from app import app


@app.route('/upload', methods=['POST'])
def upload():
    return jsonify(Controller().process_file(files=request.files))


@app.route('/query', methods=['POST'])
def query():
    data = request.json
    return jsonify(Controller().query(history=data['messages']))
