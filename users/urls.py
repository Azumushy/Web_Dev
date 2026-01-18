from django.urls import path
from .views import RegisterView, LoginView, LogoutView, SearchUsers

urlpatterns = [
path('register/', RegisterView.as_view()),
path('login/', LoginView.as_view()),
path('logout/', LogoutView.as_view()),
path('search/', SearchUsers.as_view()),
]