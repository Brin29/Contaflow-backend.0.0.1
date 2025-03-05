from django.urls import path
from .views import Home, RegisterView ,AdminView, sendEmail,ClientView

urlpatterns = [
    path('', Home.as_view()),
    path('register/', RegisterView.as_view()),
    path('admin/', AdminView.as_view()),
    path('cliente/', ClientView.as_view()),
    path('email/', sendEmail.as_view())
]