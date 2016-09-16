import re

from datadog import statsd


class Metric(object):
    def __init__(self, config: dict):
        self.name = config['name']
        self.tags = config.get('tags')

    @staticmethod
    def _fill_value(value, data: dict) -> str:
        def _format_replacer(match_obj):
            v = match_obj.group(0)[1:]
            to_work = data
            for cur_name in v.split('__'):
                to_work = to_work[cur_name]
            return str(to_work)

        return re.sub('\$[\w_\d]*\\b', _format_replacer, value)

    def _prepare_tags(self, data):
        if not self.tags:
            return None
        else:
            return [Metric._fill_value(v, data) for v in self.tags]

    def on_log(self, data: dict):
        raise NotImplementedError()


class CounterMetric(Metric):
    def on_log(self, data: dict):
        statsd.increment(Metric._fill_value(self.name, data), tags=self._prepare_tags(data))


def create_metric(type_, config) -> Metric:
    if type_ == 'counter':
        return CounterMetric(config)
    else:
        raise NotImplementedError()
