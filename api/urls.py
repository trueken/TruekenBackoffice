from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contracts', views.contracts, name='contracts'),
    path('contract/<address>', views.contract, name='contract'),
    path('trades/<address>', views.trades, name='trades'),
]