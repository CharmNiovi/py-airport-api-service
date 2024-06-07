from django.contrib import admin
from django.urls import include, path

from core.settings import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
]

if DEBUG:
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
