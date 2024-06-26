from enum import Enum
import uuid
import time


class MetricType(Enum):
    """The available prometheus metric types."""
    COUNTER = 'counter'
    GAUGE = 'gauge'
    HISTOGRAM = 'histogram'
    SUMMARY = 'summary'


class MetricLabels:

    def __init__(self):
        """New instance, empty dict."""
        self.labels = {}

    def __str__(self):
        """Join all labels and wraps them in curly braces."""
        labels = ','.join([f'{name}="{value}"' for name, value in self.labels.items()])
        return '{' + labels + '}'

    def add(self, name, value):
        """Add label to the dict."""
        self.labels.update({name: value})

    def sort(self):
        """Sort the labels alphabetically."""
        self.labels = dict(sorted(self.labels.items()))


def dict_to_metric(obj: dict):
    """Create a metric from a dictionary, coming from the rest endpoints."""
    return Metric(name=obj['name'] if 'name' in obj else None,
                  metric_type=obj['metric_type'] if 'metric_type' in obj else None,
                  description=obj['description'] if 'description' in obj else None,
                  value=obj['value'] if 'value' in obj else None,
                  labels=obj['labels'] if 'labels' in obj else None,
                  timestamp=obj['timestamp'] if 'timestamp' in obj else None,
                  print_timestamp=obj['print_timestamp'] if 'print_timestamp' in obj else None)


def default_metric():
    """Creates default metric instance."""
    labels = [{'app': 'prometheus-metric-mock-server'}]
    return Metric(name='prometheus_metric_mock_server_up',
                  metric_type=MetricType.GAUGE,
                  description='Default prometheus metric mock server metric',
                  value=1,
                  labels=labels,
                  timestamp=None,
                  print_timestamp=True)


class Metric:
    def __init__(self, name: str, metric_type: MetricType, description: str, value: float, labels: list,
                 timestamp, print_timestamp: bool):
        """Creates metric instance."""
        # Metric name or default mock_null_metric.
        self.name = name if name is not None else 'mock_null_metric'
        # Metric type or default GAUGE.
        self.metric_type = MetricType(metric_type) if metric_type is not None else MetricType.GAUGE
        # Value of the metric or default 0.0.
        self.value = value if value is not None else 0.0
        # Description if provided or default metric name followed by mock.
        self.description = description if description is not None else f'{self.name} mock'
        # At least provide empty labels object.
        labels_object = MetricLabels()
        if labels is not None:
            [labels_object.add(name, value) for label in labels for name, value in label.items()]
        self.labels = labels_object
        # If null is provided, we set it to current time.
        self.timestamp = timestamp if timestamp is not None else int(round(time.time() * 1000))
        # Usually we don't need timestamp, default is False.
        self.print_timestamp = print_timestamp if print_timestamp is not None else False
        # Sort the labels alphabetically so we have consistent unique_id_str.
        self.labels.sort()
        # Metrics are unique by name and labels.
        self.unique_id_str = f'{self.name}{self.labels}'
        # Metrics uuid based on unique_id_str.
        self.unique_id = self.get_metric_uuid()

    def get_metric_uuid(self):
        """Generate UUID for the metric based on its unique id string."""
        return str(uuid.uuid5(uuid.NAMESPACE_URL, self.get_unique_id_string()))

    def get_unique_id_string(self):
        """Return the unique id string"""
        return f'{self.name}{self.labels}'

    def get_unique_id(self):
        """Return the unique id"""
        return f'{self.unique_id}'

    def prometheus_header(self):
        """Returns the metric header in prometheus format."""
        return \
            f'# HELP {self.name} {self.description}\n' \
            f'# TYPE {self.name} {self.metric_type.value}\n'

    def prometheus_value(self):
        """Returns the metric - its name, labels, value and timestamp if required."""
        ts = self.timestamp if self.print_timestamp else ""
        return f'{self.name}{self.labels} {self.value} {ts}\n'

    def __str__(self):
        return f'{self.unique_id_str} ({self.unique_id})'
