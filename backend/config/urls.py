from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Agency Website Administration"
admin.site.site_title = "Agency Admin"
admin.site.index_title = "Website Content Management"

urlpatterns = [path("admin/", admin.site.urls), path("api/", include("core.urls"))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
