from multiprocessing import context

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from apps.clients.models import Builder, Lot, Subdivision
from apps.core.utils import group_check


class BuilderListView(UserPassesTestMixin, View):
    def test_func(self):
        check_groups = [
            'Administrators',
            'Project Managers',
        ]
        return group_check(self, check_groups=check_groups)

    page_title = "Builders"
    dash_name = page_title
    builders = Builder.objects.filter(is_active=True)
    template_name = "clients/builder_list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": self.page_title,
            "builders": self.builders,
            "dash_name": self.dash_name,
        }
        return render(request, self.template_name, context)


class BuilderDetailView(DetailView):
    model = Builder
    template_name = "clients/builder_detail.html"
    page_title = "Builders"
    dash_name = page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = context["builder"].name
        context["dash_name"] = self.dash_name
        return context
