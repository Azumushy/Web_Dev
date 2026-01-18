from django.contrib import admin
from django.urls import path, include
from users import views_pages

urlpatterns = [
path('admin/', admin.site.urls),
path('api/', include('users.urls')),
path('login/', views_pages.login_page),
path('register/', views_pages.register_page),
path('search/', views_pages.search_page),
]
