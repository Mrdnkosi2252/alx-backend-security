from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from .utils import get_ip_location
import logging


logger = logging.getLogger(__name__)


def get_rate(group, request):
    if request.user.is_authenticated:
        return '10/m'  
    return '5/m'  

@ratelimit(key='ip', rate=get_rate, method='GET', block=True)
def sensitive_view(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    location = get_ip_location(ip)

    
    logger.info(f"Sensitive view accessed by IP {ip} from {location.get('city')}, {location.get('country')}")

    
    return HttpResponse(
        f"This is a sensitive endpoint. Your IP: {ip}, Location: {location.get('city')}, {location.get('country')}"
    )

def track_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    location = get_ip_location(ip)
    return HttpResponse(f"IP: {ip}, Location: {location}")
