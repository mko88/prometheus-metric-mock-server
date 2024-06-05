from flask import Flask, request, make_response, __version__
from metric import Metric
from store import Store
import json

STORE = Store()
app = Flask(__name__)


@app.route('/metrics', methods=['GET'])
def get_metrics():
    response = make_response(STORE.export(), 200)
    response.mimetype = 'text/plain'
    return response


@app.route('/add', methods=['POST'])
def add_metrics():
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
    request_data = json.loads(request.data)
    for name in request_data:
        STORE.remove(unique_id_str=name)
    return make_response('OK', 200)


if __name__ == '__main__':
    print(__version__)
    app.run(host='0.0.0.0')


