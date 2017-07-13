from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^list(\d+)_(\d+)/$', views.list),
    url(r'^(\d+)/$',views.detail),
    url(r'^number/$',views.numbers),
    url(r'^search/$',views.MySearchView.as_view(),name='search_view'),
    url(r'^comment/',views.comment),
    url(r'^thumb_up/',views.thumb_up),

]