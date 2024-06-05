from flask import Flask, request, make_response
from metric import Metric
from store import Store
import json

# Store all metrics into the store object.
STORE = Store()
# The flask application.
app = Flask(__name__)


@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Returns all available metrics."""
    # Make the response from store content
    response = make_response(STORE.export(), 200)
    # We need it as simple text
    response.mimetype = 'text/plain'
    return response


@app.route('/add', methods=['POST'])
def add_metrics():
    """Add metric request."""
    request_data = json.loads(request.data)
    for metric in request_data:
        STORE.upsert(Metric(name=metric['name'],
                            metric_type=metric['metric_type'],
                            description=metric['description'],
                            value=metric['value'],
                            labels=metric['labels'],
                            timestamp=metric['timestamp'],
                            print_timestamp=metric['print_timestamp']))
    return make_response('OK', 200)


@app.route('/remove', methods=['POST'])
def remove_metrics():
    """Removes a metric by its readable unique id string - name{label=\"value\"}."""
    request_data = json.loads(request.data)
    for name in request_data:
        STORE.remove(unique_id_str=name)
    return make_response('OK', 200)


if __name__ == '__main__':
    """Run the application."""
    app.run(host='0.0.0.0')
