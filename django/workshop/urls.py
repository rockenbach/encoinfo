from django.conf.urls import url

from views import WorkshopList, WorkshopDetail

urlpatterns = [
    url(r'^$', WorkshopList.as_view(), name='lista'),
    url(r'^detalhe/(?P<slug>[\w-]+)/$', WorkshopDetail.as_view(), name='detalhe')
]
