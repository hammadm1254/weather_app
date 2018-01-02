from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^historical_data/(?P<lat>[+-]?\d+\.\d+),(?P<lng>[+-]?\d+\.\d+)$', views.historical_data_view, name='historical_data'),
    url(r'^create_account/$', views.create_account_view, name='create_account'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^location/(?P<pk>\d+)/$', views.location_detail, name='location_detail'),
    url(r'^history/$', views.search_list, name='search_list'),
    url(r'^$', views.home, name='home')
]