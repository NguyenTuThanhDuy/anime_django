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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# API Schema and Documentation URLs
api_schema_patterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# App-specific API Routes
api_v1_patterns = [
    path("auth/", include(("authentication.urls", "authentication"), namespace="auth")),  # Authentication APIs
    path("library/", include(("library.urls", "library"), namespace="library")),          # Library APIs
    path("", include(api_schema_patterns)),                                              # API schema and docs
]

# Main URL Patterns
urlpatterns = [
    path("admin/", admin.site.urls),             # Admin routes
    path("api/v1/", include(api_v1_patterns)),   # API v1 routes
]
