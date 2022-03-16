from django.urls import include, path

from .views import BuilderDetailView, BuilderListView

app_name = "builders"
urlpatterns = [
    path("", BuilderListView.as_view(), name="list"),
    path("view/<int:pk>/", BuilderDetailView.as_view(), name="view"),
]
