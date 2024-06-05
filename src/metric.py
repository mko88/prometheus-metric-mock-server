from enum import Enum
import uuid
import time


class MetricType(Enum):
    COUNTER = 'counter'
    GAUGE = 'gauge'
    HISTOGRAM = 'histogram'
    SUMMARY = 'summary'


class MetricLabels:

    def __init__(self):
        self.labels = {}

    def __str__(self):
        labels = ','.join([f'{k}="{v}"' for k, v in self.labels.items()])
        return '{' + labels + '}'

    def add(self, name, value):
        self.labels.update({name: value})

    def sort(self):
        self.labels = dict(sorted(self.labels.items()))


def get_metric_uuid(unique_id_str: str):
    return uuid.uuid5(uuid.NAMESPACE_URL, unique_id_str)


def default_metric():
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
        labels_object = MetricLabels()
        if labels is not None:
            [labels_object.add(name, value) for label in labels for name, value in label.items()]
        self.name = name if name is not None else 'mock_null_metric'
        self.metric_type = MetricType(metric_type) if metric_type is not None else MetricType.GAUGE
        self.value = value if value is not None else 0.0
        self.description = description if description is not None else 'mock'
        self.labels = labels_object
        self.timestamp = timestamp if timestamp is not None else int(round(time.time() * 1000))
        self.print_timestamp = print_timestamp if print_timestamp is not None else False

        self.labels.sort()
        # Metrics are unique by name and labels
        self.unique_id_str = f'{name}{self.labels}'
        self.unique_id = get_metric_uuid(self.unique_id_str)

    def prometheus_header(self):
        return \
            f'# HELP {self.name} {self.description}\n' \
            f'# TYPE {self.name} {self.metric_type.value}\n'

    def prometheus_value(self):
        ts = self.timestamp if self.print_timestamp else ""
        return f'{self.name}{self.labels} {self.value} {ts}\n'
