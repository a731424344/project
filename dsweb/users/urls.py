from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^login/$',views.login),
    url(r'^verify/$',views.verify_code),
    url(r'^info_handle/$',views.info_handle),
    url(r'^re_name/$',views.re_name)

]