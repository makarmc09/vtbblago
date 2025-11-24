from django.contrib import admin
from django.urls import path
from VTBBlago import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("projects/", views.projects, name="projects"),
    path("pay/<int:project_id>/", views.pay, name="pay"),
    path("about/", views.about, name="about"),
    path("help/", views.help_request, name="help"),
    path("help/form/", views.help_form, name="help_form"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
]
