from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<uuid:user_id>/', views.UserDetailAdminView.as_view(), name='user-detail'),
    path('freelancers/search/', views.FreelancerSearchView.as_view(), name='freelancer-search'),
]
