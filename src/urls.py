
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('suppliers/', include('suppliers.urls')),

    # Django admin site url
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
