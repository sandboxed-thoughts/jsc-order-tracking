from django.urls import include, path

from .views import BuilderDetailView, BuilderListView

app_name = "clients"
urlpatterns = [
    path("builders/list/", BuilderListView.as_view(), name="builder_list"),
    path("builders/view/<slug:slug>/", BuilderDetailView.as_view(), name="builder_view"),
]
