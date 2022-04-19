from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "app_base"

urlpatterns = [
    path("", views.Index_ListView.as_view(), name="Index_ListView_name"),
    path(
        "task/<int:pk>/", views.Task_DetailView.as_view(), name="Task_DetailView_name"
    ),
    path("create/", views.Form_CreateView.as_view(), name="Form_CreateView_name"),
    path(
        "update/<int:pk>/", views.Form_UpdateView.as_view(), name="Form_UpdateView_name"
    ),
    path(
        "delete/<int:pk>/", views.Form_DeleteView.as_view(), name="Form_DeleteView_name"
    ),
    ########################
    path("login/", views.Custom_LoginView.as_view(), name="Custom_LoginView_name"),
    path("logout",LogoutView.as_view(next_page="app_base:Index_ListView_name"), name="LogoutView_name"),
    path("register",views.Custom_Register.as_view(), name="Custom_Register_name"),
]
