from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('DesertTraders.web_generic_features.urls')),
                  path('accounts/', include('DesertTraders.users.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'DesertTraders.web_generic_features.views.main.not_found_view'
handler400 = 'DesertTraders.web_generic_features.views.main.bad_request_view'