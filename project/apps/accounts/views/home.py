

from random import random
from django import views
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    """
    View to render the homepage. Login is required to reach the home view
    """
    page_title = "Home"
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
