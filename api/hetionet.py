import logging
import os

from flask import Flask, render_template, request
from flask_restx import Resource, Api
from utils.reader import read_text, read_text_from_disk

LOG = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

@api.route('/v1/diseases/<string:id>')
class Disease(Resource):
    def post(self, id):
        return id

@api.route('/v1/treatments/<string:disease_id>')
class Treatment(Resource):
    def post(self, disease_id):
        return disease_id


@app.route('/home')
def index():
    node_list = read_text_from_disk("hetionet-v1.0-nodes.tsv", delimiter='\t', skip_header=False)
    diseases = [node.get('id') for node in node_list if node.get('id').startswith('Disease')]
    return render_template('index.html', diseases=["Disease::DOID:9970"] + diseases)

