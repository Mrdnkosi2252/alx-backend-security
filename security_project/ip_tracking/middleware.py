from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
from ipware import get_client_ip
from .models import RequestLog, BlockedIP
from django_ip_geolocation.backends import IPGeolocationAPI

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip, is_routable = get_client_ip(request)
        if client_ip and is_routable:
            if BlockedIP.objects.filter(ip_address=client_ip).exists():
                return HttpResponseForbidden("Access forbidden: Your IP is blacklisted.")
            
            geo_key = f'geo_{client_ip}'
            geo = cache.get(geo_key)
            if geo is None:
                backend = IPGeolocationAPI(api_key=getattr(settings, 'IP_GEOLOCATION_API_KEY', ''))
                location = backend.geolocate(client_ip)
                geo = {
                    'country': getattr(location, 'country_name', ''),
                    'city': getattr(location, 'city', '')
                }
                cache.set(geo_key, geo, 86400)  # 24 hours
            
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path,
                country=geo['country'],
                city=geo['city']
            )
        response = self.get_response(request)
        return response