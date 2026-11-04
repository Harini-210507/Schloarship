from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import StudentRegistrationForm, StudentLoginForm, StudentProfileForm
from .models import StudentProfile


# ── Decorators ──────────────────────────────────────────────────────────────

def student_required(view_func):
    """Allow access only to authenticated, non-staff users (students)."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.is_staff:
            return redirect('administrator:dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def admin_required(view_func):
    """Allow access only to staff users (administrators)."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_staff:
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── Auth Views ───────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:student_dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated student profile
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard:student_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('administrator:dashboard')
        return redirect('dashboard:student_dashboard')

    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            if user.is_staff:
                return redirect('administrator:dashboard')
            return redirect('dashboard:student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = StudentLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('home')


# ── Student Dashboard ────────────────────────────────────────────────────────

@student_required
def student_dashboard(request):
    from applications.models import ScholarshipApplication
    applications = ScholarshipApplication.objects.filter(
        student=request.user
    ).select_related('scholarship').order_by('-submitted_at')

    context = {
        'applications': applications,
        'total': applications.count(),
        'submitted': applications.filter(status='submitted').count(),
        'under_review': applications.filter(status='under_review').count(),
        'approved': applications.filter(status='approved').count(),
        'rejected': applications.filter(status='rejected').count(),
    }
    return render(request, 'accounts/student_dashboard.html', context)


# ── Profile ──────────────────────────────────────────────────────────────────

@student_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


# ── Error Handlers ───────────────────────────────────────────────────────────

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
