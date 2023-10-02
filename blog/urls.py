from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("blog/", views.index, name="main"),
    path("blog/post-<str:title>/", views.post, name="post"),
    path("about", views.about, name="about"),
    path("contacts", views.contacts, name="contacts"),
    path("services", views.services, name="services"),
    path('blog/category/<str:name>', views.category, name='category'),
    path("blog/search/",views.search,name='search'),
    path("blog/create/",views.create,name="create"),
    path("blog/login",LoginView.as_view(),name="blog_login"),
    path("blog/logout",LogoutView.as_view(),name="blog_logout"),
    path("blog/profile",views.profile,name="profile"),
    path("blog/edit_profile",views.edit_profile,name="editProfile"),
    path("blog/register",views.registration_user,name="register")
    # path("<dynamic_url>", views.pro_url, name="test"),
]

