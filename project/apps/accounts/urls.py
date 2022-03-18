from django.urls import include, path
from .forms import UserLoginForm
from .views import CustomLoginView, CustomLogoutView, HomeView

app_name = 'accounts'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
