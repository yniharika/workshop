
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Student
from .ai_utils import explain_topic


# Home Page
def home(request):
    return render(request, 'companion_app/home.html')


# Student Registration
def register_view(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        course = request.POST.get('course', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([full_name, username, email, course, password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        elif Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')

        else:
            try:
                validate_password(password)

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                Student.objects.create(
                    user=user,
                    full_name=full_name,
                    email=email,
                    course=course
                )

                login(request, user)
                return redirect('dashboard')

            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)

    return render(request, 'companion_app/register.html')


# Student Login
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'companion_app/login.html')


# Student Logout
def logout_view(request):
    logout(request)
    return redirect('home')


# Student Dashboard
@login_required(login_url='login')
def dashboard(request):

    student = Student.objects.get(user=request.user)

    return render(
        request,
        'companion_app/dashboard.html',
        {'student': student}
    )

@login_required(login_url='login')
def topic_explainer(request):
    explanation = ""
    topic = ""

    if request.method == "POST":
        topic = request.POST.get("topic", "").strip()

        if topic:
            explanation = explain_topic(topic)

    return render(
        request,
        "companion_app/topic_explainer.html",
        {
            "topic": topic,
            "explanation": explanation
        }
    )

