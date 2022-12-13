from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name='index'),
    path("user",user_form,name='user-details'),
    path("user-pay/<int:id>",insure_pay,name='insure_pay'),
    path("dash",dash,name='dash'),
    path("clime",clime_insure,name='clime'),
    path("login",user_login,name='login'),
    path("logout",user_logout,name='logout'),

    path("register",user_register,name='register'),

]