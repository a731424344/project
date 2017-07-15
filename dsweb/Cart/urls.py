from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^add/$',views.add),
    url(r'^count/',views.count),
    url(r'^$',views.index),
    url(r'^save_count/$',views.save_count),
    url(r'^del/$',views.delete),
    url(r'^order/$',views.order),


]