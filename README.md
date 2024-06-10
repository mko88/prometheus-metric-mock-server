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
Default index page. Just prints a message
## GET /metrics
The mocked metrics in Prometheus format.
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
mock_null_metric{label="value"} 42.0 
```
## POST /metrics
Add metrics that will be returned by the `/metrics` GET endpoint.<br>
<b>Description and type hints are taken from the first found metric internally.
Make sure you always use the same <i>description</i> and <i>metric_type</i> per <i>name</i> to avoid confusion.</b>
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
<li>The labels will always be sorted by their name in alphabetical order.

## DELETE /metrics
Removes metrics by name and labels. Same structure like the POST request can be used.
<li>The unique string identifier of a metric consist of its name and labels. All other fields are ignored.

```json
[
    {
        "name": "prometheus_metric_mock_server_up",
        "labels": [
            {"app": "prometheus-metric-mock-server"}
        ]
    }
]
```

## GET /store
The store content containing the metric unique ids and strings.
```json
[
    {
        "unique_id": "1a3c07c9-d651-53a8-83ad-0ef5ceb94814",
        "unique_id_string": "prometheus_metric_mock_server_up{app=\"prometheus-metric-mock-server\"}"
    },
    {
        "unique_id": "8e9b5398-8c90-547d-8dbd-bb058936603b",
        "unique_id_string": "test_metric_name{app=\"MyApplication\",job=\"MyJob\"}"
    },
    {
        "unique_id": "60811f35-3e55-51ce-95d6-ac792682dd51",
        "unique_id_string": "mock_null_metric{}"
    }
]
```

## DELETE /remove_by_unique_id
Removes metrics by unique ids
```json
[
    "1a3c07c9-d651-53a8-83ad-0ef5ceb94814",
    "60811f35-3e55-51ce-95d6-ac792682dd51"
]
```