from django.urls import path

from .views import DashboarView, UserRegistrationView, UserLoginView, UserLogoutView, UserUpdateView, UserProfileView

app_name = 'users'


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('dashboard/', DashboarView.as_view(), name='dashboard'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('user/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='edit'),
]
