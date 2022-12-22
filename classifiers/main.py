from flask import request, abort, make_response
from flask import Flask
from flask import jsonify
import math
#from sklearn.externals import joblib
from json import dumps
from joblib import load
app = Flask(__name__)


@app.before_first_request
def load_global_data():
    global model
    model = load('baz_model.mdl')


@app.route('/')
def hello_world():
    return 'I am working!'


@app.route('/api/predict', methods=['GET'])
def predict():
    r = request.args.get('r', type=int)
    g = request.args.get('g', type=int)
    b = request.args.get('b', type=int)
    rgb = [r, g, b]
    if len([(c < 0) | (c > 255) for c in rgb]) > 0:
        bad_request('color range must be within [0, 255]')
    y_pred = model.predict([rgb])
    return y_pred.tolist()


def bad_request(message, code=400):
    abort(make_response(jsonify(message=message), code))


if __name__ == '__main__':
    app.run()