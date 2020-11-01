import logging
import os

from flask import Flask, render_template, request
from flask_restx import Resource, Api
from utils.reader import read_text, read_text_from_disk
from db.redis.redis import find_disease
from db.neo4j.neo4j import find_disease_treatments

LOG = logging.getLogger(__name__)
FILENAME = "hetionet-v1.0-nodes.tsv"
app = Flask(__name__)
api = Api(app)

@api.route('/v1/diseases/<string:id>')
class Disease(Resource):
    def post(self, id):
        result = find_disease(id)
        return result if result is not None else {}

@api.route('/v1/treatments/<string:disease_name>')
class Treatment(Resource):
    def post(self, disease_name):
        result = find_disease_treatments(disease_name)
        return result if result is not None else []


@app.route('/home')
def index():
    node_list = read_text_from_disk(FILENAME, delimiter='\t', skip_header=False)
    diseases = [node.get('id') for node in node_list if node.get('id').startswith('Disease')]
    return render_template('index.html', diseases=diseases)

