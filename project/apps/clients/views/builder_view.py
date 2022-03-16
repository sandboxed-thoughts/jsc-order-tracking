from multiprocessing import context

from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView

from apps.clients.models import Builder, Lot, Subdivision


class BuilderListView(View):
    builders = Builder.objects.all()
    template_name = "builders/builder_view_template.html"

    def get(self, request, *args, **kwargs):
        context = {"builders": self.builders}
        if request.user.is_superuser:
            context["super_intro"] = "Welcome Superuser!"
        return render(request, self.template_name, context)


class BuilderDetailView(DetailView):
    model = Builder
    template_name = "builders/builder_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
