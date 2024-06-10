from flask import Flask, request, make_response
from metric import dict_to_metric
from store import Store
import json
import logging
import sys

# Version.
version = '0.0.1'

# Setup logging level info on stdout.
root = logging.getLogger()
root.setLevel(logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Store all metrics into the store object.
STORE = Store()
# The flask application.
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Default index message"""
    return f'<h1>Python Metric Mock Server ({version}) - visit or scrape the /metrics endpoint.</h1>'


@app.route('/store', methods=['GET'])
def export_metrics_store():
    """Export the store unique ids and unique id string"""
    # Make the response from store content
    response = make_response(STORE.export(), 200)
    # JSON format
    response.mimetype = 'application/json'
    return response


@app.route('/metrics', methods=['GET'])
def export_metrics_prometheus():
    """Returns all available metrics."""
    # Make the response from store content
    response = make_response(STORE.export_prometheus(), 200)
    # We need it as simple text
    response.mimetype = 'text/plain'
    return response


@app.route('/metrics', methods=['POST'])
def add_metrics():
    """Add metric request."""
    request_data = json.loads(request.data)
    for metric_data in request_data:
        STORE.upsert(dict_to_metric(metric_data))
    return make_response('OK', 200)


@app.route('/metrics', methods=['DELETE'])
def remove_metrics():
    """Removes metrics. A whole metric object can be provided, only name and labels are used for identification."""
    request_data = json.loads(request.data)
    for metric_data in request_data:
        STORE.remove(metric=dict_to_metric(metric_data))
    return make_response('OK', 200)


@app.route('/remove_by_unique_id', methods=['DELETE'])
def remove_metrics_by_unique_id():
    """Removes a metrics by list of unique ids."""
    request_data = json.loads(request.data)
    for uid in request_data:
        STORE.remove_by_unique_id(unique_id=uid)
    return make_response('OK', 200)


if __name__ == '__main__':
    """Run the application."""
    app.run(host='0.0.0.0')
