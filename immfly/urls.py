"""
URL configuration for immfly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from media_api import views as media_api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('channels/', media_api_views.list_channels, name='list_channels'),
    path('channels/<int:pk>/', media_api_views.get_channel_by_id, name='get_channel_by_id'),
    path('channels/filter_by_group/', media_api_views.filter_channels_by_group, name='filter_channels_by_group'),
    path('channels/<int:pk>/subchannels_and_contents/', media_api_views.get_subchannels_and_contents,
         name='subchannels_and_contents'),
]
