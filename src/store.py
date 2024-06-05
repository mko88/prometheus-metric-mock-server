from metric import Metric, get_metric_uuid, default_metric


class Store:
    def __init__(self):
        """The metric store, initially contains a single default metric provided by the mock."""
        self.metrics = {}
        self.upsert(default_metric())

    def export(self):
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

    def remove(self, unique_id_str: str):
        """Remove metric from the store by unique id string."""
        unique_id = get_metric_uuid(unique_id_str)
        if unique_id in self.metrics.keys():
            self.metrics.pop(unique_id)
            print(f'Removed metric: {unique_id_str}')
        else:
            print(f'Metric does not exist. Nothing removed: {unique_id_str}')
