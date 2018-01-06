from django.urls import path
from django.views.generic import DetailView, ListView

from .models import Cup
from .views import CupCreateView, DonCreateView, DonDispatchView, DonUpdateView

app_name = 'cup'
urlpatterns = [
    path('all', ListView.as_view(model=Cup), name='home'),
    path('add', CupCreateView.as_view(), name='add'),
    path('<str:slug>', DetailView.as_view(model=Cup), name='cup'),
    path('<str:slug>/don', DonDispatchView.as_view(), name='don'),
    path('<str:slug>/don/create', DonCreateView.as_view(), name='add_don'),
    path('<str:slug>/don/<int:pk>', DonUpdateView.as_view(), name='update_don'),
]
