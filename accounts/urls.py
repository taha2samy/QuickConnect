from django.urls import path
from .views import SignUpView,LoginViewpPage


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginViewpPage.as_view(), name='login'),
]
