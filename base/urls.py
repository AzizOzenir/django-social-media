from django.urls import path
from base import views

urlpatterns = [
    path("",views.index,name="index"),
    path("signup",views.signup,name="signup"),
    path("upload",views.upload,name="upload"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("settings",views.settings,name="settings"),
    path("profile/<str:pk>",views.profile,name="profile"),
    path("like",views.like,name="like"),
    path("delete_post",views.delete_post,name="delete_post"),
    path('follow', views.follow, name='follow'),
    path('search/', views.search, name='search'),

]