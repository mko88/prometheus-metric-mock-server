# What is this
prometheus-metric-mock-server is small flask application that can 
simulate prometheus metrics and be scraped by a prometheus server.

By default, the `prometheus_metric_mock_server_up` metric is provided.
You can be removed with the `/remove` endpoint.
## Requirements
The application is written on python 3.8 and uses flask 3.0.3 bit it will
probably work just fine with different versions.
## Configuration
Currently, there is no configuration available.

# How to use
## Run
```bash
python3 main.py
```
## Docker
```bash
docker build -t prometheus-metric-mock-server .
docker run --rm -p 5000:5000 prometheus-metric-mock-server
```
After the application is running you should be able to access it at `localhost:5000`.
# Endpoints
## GET /
The index page.
## GET /metrics
The mocked metrics that can be scraped by prometheus.
## POST /add
Add metrics that will be returned by the `/metrics` endpoint.
```json
[
    {
        "name": "test_metric_name",
        "metric_type": "gauge",
        "description": "Free text description",
        "value": 1.0,
        "timestamp": 1717605371612,
        "print_timestamp": false,
        "labels": [
            {"job": "MyJob"},
            {"app": "MyApplication"}
        ]
    },
    {
        "name": null,
        "metric_type": null,
        "description": null,
        "value": null,
        "timestamp": null,
        "print_timestamp": null,
        "labels": []
    }
]
```
<li>All fields must be provided. 
<li><b>null</b> values can be provided for all fields 
except `labels` - it must be at least empty array.
<li>Possible values for the metric_type are <b>gauge</b>,<b>counter</b>,<b>histogram</b> 
and <b>summary</b>. Default value is gauge, other values will cause runtime exception.
<li>The labels will always be sorted by their name in alphabetical order.<br><br>

The request above will produce the following metrics on the `/metrics` endpoint.<br>
<b>***</b> Note that the `prometheus_metric_mock_server_up` is added on startup with current time
and the `print_timestamp` field is set to `true`.
```
# HELP prometheus_metric_mock_server_up Default prometheus metric mock server metric
# TYPE prometheus_metric_mock_server_up gauge
prometheus_metric_mock_server_up{app="prometheus-metric-mock-server"} 1 1717607477405
# HELP test_metric_name Free text description
# TYPE test_metric_name gauge
test_metric_name{app="MyApplication",job="MyJob"} 1.0
# HELP mock_null_metric mock_null_metric mock
# TYPE mock_null_metric gauge
mock_null_metric{} 0.0 
```
## POST /remove
Removes metric by its unique string identifier. 
<li>The unique string identifier of a metric consist of its name and labels.
<li>The labels <b>must</b> be sorted in alphabetical order.

```json
[
    "test_metric_name{app=\"MyApplication\",job=\"MyJob\"}",
    "prometheus_metric_mock_server_up{app=\"prometheus-metric-mock-server\"}"
]
```