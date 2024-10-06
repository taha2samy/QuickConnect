from django.shortcuts import render
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = 'Home'
    template_name="logout.html"  

class SignUpView(AccessMixin, TemplateView):
    template_name = 'signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login')  # Redirect if the user is logged in
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Get data from form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the same username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return self.render_to_response(self.get_context_data())

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return self.render_to_response(self.get_context_data())

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Add a success message and redirect
        messages.success(request, "Sign-up successful! You can now log in.")
        return redirect('login')  
    
class LoginViewpPage(LoginView):
    template_name = 'login.html'  # Your login template
    redirect_authenticated_user = True  # Redirects logged-in users

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")  # Handle login failure
        return super().form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "You have successfully logged in.")  # Handle successful login
        return reverse_lazy('Home')  # Redirect to home or dashboard after login
