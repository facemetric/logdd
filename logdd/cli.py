#!/usr/bin/env python3
import subprocess
import threading

import click
import yaml

from logdd.dd import create_metric, Metric
from logdd.parse import load_pattern, FormatSpec


@click.group()
def cli():
    pass


def __tail(file_name, metric: Metric, format_parser: FormatSpec):
    def _run_tail():
        f = subprocess.Popen(['tail', '-f', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            data = format_parser.parse(f.stdout.readline().decode('utf-8'))
            if data:
                metric.on_log(data)

    thread = threading.Thread(target=_run_tail)
    thread.start()
    return thread


@cli.command('daemon', help='Start process to monitor logs')
@click.option('--config', help='Path to configuration file')
def daemon(config: str):
    config = yaml.load(open(config, 'r'))
    formats = {k: load_pattern(v) for k, v in config['formats'].items()}
    metrics = {k: create_metric(v['type'], v['config']) for k, v in config['metrics'].items()}

    threads = [__tail(log['file'], metrics[log['metric']], formats[log['format']]) for log in config['logs']]

    # Signal handler


if __name__ == '__main__':
    cli()
