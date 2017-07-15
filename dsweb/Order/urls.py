from django.conf.urls import url
import views
urlpatterns = [
    url('^order/',views.do_order),

]