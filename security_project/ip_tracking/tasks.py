from celery import shared_task
from django.utils import timezone
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
    
    high_request_ips = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
        .values('ip_address') \
        .annotate(request_count=Count('id')) \
        .filter(request_count__gt=100)
    
    for entry in high_request_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': f"High request count: {entry['request_count']} requests in the last hour"}
        )
    
    sensitive_paths = ['/admin/', '/login/']
    sensitive_ips = RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=sensitive_paths) \
        .values('ip_address') \
        .annotate(access_count=Count('id')) \
        .filter(access_count__gt=10)
    
    for entry in sensitive_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': f"Suspicious access to sensitive paths: {entry['access_count']} times in the last hour"}
        )