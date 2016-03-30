from django.conf.urls import url
from django.views.generic import DetailView, ListView

from .models import Cup
from .views import CupCreateView, DonCreateView, DonDispatchView, DonUpdateView

app_name = 'cup'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Cup), name='home'),
    url(r'^add$', CupCreateView.as_view(), name='add'),
    url(r'^cup/(?P<slug>[^/]+)$', DetailView.as_view(model=Cup), name='cup'),
    url(r'^cup/(?P<slug>[^/]+)/don$', DonDispatchView.as_view(), name='don'),
    url(r'^cup/(?P<slug>[^/]+)/don/create$', DonCreateView.as_view(), name='add_don'),
    url(r'^cup/(?P<slug>[^/]+)/don/(?P<pk>\d+)$', DonUpdateView.as_view(), name='update_don'),
]
