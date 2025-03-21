from django.urls import path
from .views import UserView,  UsersView, RegisterView , ChangePassword,sendEmail, CustomTokenObtainPairView
urlpatterns = [
    path('users/<int:user_id>/', UserView.as_view()),
    path('users/', UsersView.as_view()),
    path('register/', RegisterView.as_view()),
    path('email/', sendEmail.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('password/', ChangePassword.as_view())
]