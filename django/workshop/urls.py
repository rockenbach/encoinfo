from django.conf.urls import url

from views import WorkshopList

urlpatterns = [
    url(r'^$', WorkshopList.as_view(), name='lista')
]
