from django.urls import path
from . import views
urlpatterns = [
    path('',views.Home,name="home"),
    path('login/',views.UserLogin,name="login"),
    path('register/',views.UserRegister,name="register"),
    path('logout/',views.UserLogout,name="logout")
]
