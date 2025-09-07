from django.urls import path
from .views import sensitive_view, track_ip 

urlpatterns = [
    path('secure/', sensitive_view),
    path('track/', track_ip),
]
