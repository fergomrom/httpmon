from httpmon.data.alerts import RequestsAlert
from httpmon.data.metrics import (IPMetric, MethodMetric, MetricSummary,
                                  SectionMetric, StatusCodeMetric)

available_metrics = {
    'section': {
        'class': SectionMetric,
        'description': 'Sections with most hits',
    },
    'ip_address': {
        'class': IPMetric,
        'description': 'IP addresses',
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
