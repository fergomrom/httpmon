from httpmon.data.alerts import RequestsAlert
from httpmon.data.metrics import (HostMetric, MethodMetric, MetricSummary,
                                  SectionMetric, StatusCodeMetric)

available_metrics = {
    'section': {
        'class': SectionMetric,
        'description': 'Sections with most hits',
    },
    'remotehost': {
        'class': HostMetric,
        'description': 'Remote IP and hostnames with most hits',
    },
    'status_code': {
        'class': StatusCodeMetric,
        'description': 'Most seen status codes',
    },
    'method': {
        'class': MethodMetric,
        'description': 'Most seen HTTP methods',
    },
    'summary': {
        'class': MetricSummary,
        'description': 'Summary statistics',
    },
}

available_alerts = {
    'requests': {
        'class': RequestsAlert,
        'description': 'Total requests per second above threshold',
    }
}
