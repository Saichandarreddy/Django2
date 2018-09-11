from django.conf.urls import url, include
from rest_framework import routers
from api import views
from django.conf.urls.static import static
from django import views
from django.conf import settings

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^web/(?P<path>.*)$',views.static.serve,{'document_root': settings.STATIC_ROOT})
]#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
