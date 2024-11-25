"""
URL configuration for anime_library project.

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
from django.urls import path

from library import views

urlpatterns = [
    path('videos', views.get_videos, name="videos"),
    path('channels/<uuid:channel_id>', views.get_channel_by_id_api, name='get_channel_by_id'),
    path('channels/', views.get_channels_by_ids_api, name='get_channels_by_ids'),
    path('channels/create', views.create_channel, name='create_channel'),
    path('channels/<uuid:channel_id>/edit', views.edit_channel, name='edit_channel'),
]
