from django.conf.urls import url
from django.views.generic import ListView, DetailView, CreateView

from .models import Cup, Don
from .views import DonCreateView

app_name = 'cup'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Cup), name='home'),
    url(r'^cup$', CreateView.as_view(model=Cup), name='add_cup'),
    url(r'^(?P<slug>[^/]+)$', DetailView.as_view(model=Cup), name='cup'),
    url(r'^(?P<slug>[^/]+)/dette$', DonCreateView.as_view(), name='don'),
]
