from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class Index_ListView(LoginRequiredMixin, ListView):
    model = models.Tasks
    template_name = "app_base/index.html"  # default tasks_list.html   (tasks) model sonuna _list.html
    context_object_name = "tasks"  # default object_list  (template giden context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()

        custom_filter = self.request.GET.get("text_search_input") or ""
        if custom_filter:
            context["tasks"] = context["tasks"].filter(title__icontains=custom_filter)
        context["custom_filter"] = custom_filter

        return context


class Task_DetailView(LoginRequiredMixin, DetailView):
    model = models.Tasks
    template_name = "app_base/detail.html"
    context_object_name = "thetask"


class Form_CreateView(LoginRequiredMixin, CreateView):
    model = models.Tasks
    fields = ["title", "description", "complete"]
    template_name = "app_base/create.html"
    context_object_name = "form"
    success_url = reverse_lazy("app_base:Index_ListView_name")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Form_CreateView, self).form_valid(form)


class Form_UpdateView(LoginRequiredMixin, UpdateView):
    model = models.Tasks
    fields = ["title", "description", "complete"]
    template_name = "app_base/update.html"
    context_object_name = "form"
    success_url = reverse_lazy("app_base:Index_ListView_name")


class Form_DeleteView(LoginRequiredMixin, DeleteView):
    model = models.Tasks
    template_name = "app_base/delete.html"
    context_object_name = "form"
    success_url = reverse_lazy("app_base:Index_ListView_name")


###############################################################################


class Custom_LoginView(LoginView):
    template_name = "app_base/login.html"
    # success_url = reverse_lazy("app_base:Index_ListView_name")
    # context_object_name = "form"  bu galiba bu viewde yok
    def get_success_url(self):
        return reverse_lazy("app_base:Index_ListView_name")


class Custom_Register(FormView):
    template_name = "app_base/register.html"
    success_url = reverse_lazy("app_base:Index_ListView_name")
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return super(Custom_Register, self).form_valid(form)

    def get(
        self, *args, **kwargs
    ):  # çünkü register sayfasına gelince yönlendirmesi için, eğer giriş yapılmışsa
        if self.request.user.is_authenticated:
            return redirect("app_base:Index_ListView_name")
        return super(Custom_Register, self).get(*args, **kwargs)
