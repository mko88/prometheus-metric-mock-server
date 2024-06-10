from metric import Metric, default_metric
import json


class Store:
    def __init__(self):
        """The metric store, initially contains a single default metric provided by the mock."""
        self.metrics = {}
        self.upsert(default_metric())

    def export(self):
        """Export the metric store with uid and uid string representation."""
        output = []
        for metric in self.metrics.values():
            output.append({'unique_id': metric.unique_id, 'unique_id_string': metric.unique_id_str})
        return json.dumps(output)

    def export_prometheus(self):
        """Export the store content to string that can be scraped by Prometheus."""
        output = ''
        # Gather unique metric names.
        metric_names = set(metric.name for metric in self.metrics.values())
        for metric_name in metric_names:
            # Gather all metrics for name.
            metrics = [metric for metric in self.metrics.values() if metric.name == metric_name]
            # Append prometheus header from first metric. Others will be ignored.
            output += metrics[0].prometheus_header()
            for metric in metrics:
                # Append all metrics below the header.
                output += metric.prometheus_value()
        return output

    def upsert(self, metric: Metric):
        """Insert or update metric to the store."""
        if metric.unique_id in self.metrics.keys():
            print(f'Updating metric: {metric.unique_id_str} {metric.value}')
        else:
            print(f'Adding metric: {metric.unique_id_str} {metric.value}')
        self.metrics.update({metric.unique_id: metric})

    def remove_by_unique_id(self, unique_id: str):
        """Remove metric from the store by unique id."""
        if unique_id in self.metrics.keys():
            removed_metric = self.metrics.pop(unique_id)
            print(f'Removed metric by uid {unique_id}: {removed_metric.unique_id_str}')
        else:
            print(f'Metric not found by {unique_id}. Nothing removed.')

    def remove(self, metric: Metric):
        """Remove metric from the store by unique id string."""
        if metric.unique_id in self.metrics.keys():
            removed_metric = self.metrics.pop(metric.unique_id)
            print(f'Removed metric by name and labels: {removed_metric.unique_id_str}. '
                  f'Unique id was {removed_metric.unique_id}')
        else:
            print(f'Metric not found by name and labels: {metric.unique_id_str}. Nothing removed.')