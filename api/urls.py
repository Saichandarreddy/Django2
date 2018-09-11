from django.conf.urls import url, include
from rest_framework import routers
from api import viewset
from django.conf.urls.static import static
from django import views
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'users', viewset.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/',viewset.login),
    url(r'^logout/',viewset.logout),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^/(?P<path>.*)$',views.static.serve,{'document_root': settings.MEDIA_ROOT})
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
