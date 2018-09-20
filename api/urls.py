from django.conf.urls import url, include
from rest_framework import routers
from django.conf.urls.static import static
from django import views
from django.conf import settings

router = routers.DefaultRouter()

from api import viewset
from api import fileviewset

#router.register(r'users', viewset.UserViewSet)
#router.register(r'file', fileviewset.ImageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/',viewset.login),
    url(r'^logout/',viewset.logout),
    url(r'^register/',viewset.createuser),
    url(r'^getFiles/',fileviewset.fileList),
    url(r'^fileUpload/',fileviewset.fileUpload),
    url(r'^fileUpdate/',fileviewset.fileUpdate),
    url(r'^fileDelete/',fileviewset.fileDelete),
    url(r'^pdfUpload/',fileviewset.pdfUpload),
    url(r'^createUser/',viewset.createuser),
    url(r'^getUsers/',viewset.getUsers),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^(?P<path>.*)$',views.static.serve,{'document_root': settings.MEDIA_ROOT})
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
