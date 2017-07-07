from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^login/$',views.login),
    url(r'^verify/$',views.verify_code),
    url(r'^info_handle/$',views.info_handle),
    url(r'^re_name/$',views.re_name),
    url(r'^suc_reg/$',views.info_handle),
    url(r'^login_handle/$',views.login_handle),
    url(r'^change_pwd/$',views.change_pwd),
    url(r'^newpwd_handle/$',views.newpwd_handle),
    url(r'^center/$',views.center),
    url(r'^order/$',views.order),
    url(r'^site/$',views.site),

]