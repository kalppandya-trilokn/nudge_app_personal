# Urls.py of your app
from django.urls import path
from .views import dashboard_view

urlpatterns = [
    # Change the name to 'dashboard'
    path("", dashboard_view, name="admin_dashboard"),
]