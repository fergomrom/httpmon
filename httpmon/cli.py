import click

from httpmon.data import available_metrics
from httpmon.main import HTTPMonCLI


def _metrics_process(ctx, param, metrics):
    metrics = [metric.strip() for metric in metrics.split(',')]
    for metric in metrics:
        if metric not in available_metrics:
            raise click.BadOptionUsage(f'{metric} is not available.')

    return metrics


@click.command()
@click.option('--log-dir', default='/tmp/access.log', help='Access log directory.')
@click.option('--max-requests', default=10, help='Maximum number of requests per second before sending an alert.')
@click.option('--refresh-frequency', default=10, help='Refresh frequency in seconds.')
@click.option(
    '--included-metrics', default=','.join(available_metrics), show_default=True,
    callback=_metrics_process, help='Comma separated list of displayed metrics.'
)
def httpmon_cli(log_dir, max_requests, refresh_frequency, included_metrics):
    httpmon_main = HTTPMonCLI(log_dir, max_requests, refresh_frequency, included_metrics)
    httpmon_main.start()
