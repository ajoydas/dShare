from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
import authentication.views  as auth

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth.home, name='home'),
    url(r'^login', auth.login_view, name='login'),
    url(r'^logout', auth.logout_view, name='logout'),
    url(r'^user/', include('user.urls')),
    url(r'^insurance/', include('insurance.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)