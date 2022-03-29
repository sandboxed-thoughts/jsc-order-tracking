from multiprocessing import context

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from apps.core.utils import group_check

from ..models import BuilderModel as Builder


class BuilderListView(UserPassesTestMixin, View):
    def test_func(self):
        check_groups = [
            "Administrators",
            "Project Managers",
        ]
        return group_check(user=self.request.user, check_groups=check_groups)

    builders = Builder.active_builders.all()

    template_name = "clients/builder_list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": self.page_title,
            "builders": self.builders,
            "dash_name": self.dash_name,
        }
        return render(request, self.template_name, context)


class BuilderDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        check_groups = [
            "Administrators",
            "Project Managers",
        ]
        return group_check(user=self.request.user, check_groups=check_groups)

    model = Builder
    template_name = "clients/builder_detail.html"
    page_title = "Builders"
    dash_name = page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = context["builder"].name
        context["dash_name"] = self.dash_name
        return context
