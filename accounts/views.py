from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm, ProfileForm
from accounts.models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('enrollments:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Xush kelibsiz, {user.first_name}! Ro\'yxatdan muvaffaqiyatli o\'tdingiz.')
            return redirect('enrollments:dashboard')
        else:
            messages.error(request, 'Iltimos, xatolarni to\'g\'rilang.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('enrollments:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Email orqali ham login qilish imkoni
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Xush kelibsiz, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'enrollments:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol noto\'g\'ri.')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Tizimdan muvaffaqiyatli chiqdingiz.')
        return redirect('courses:home')
    return redirect('courses:home')


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # User modelini ham yangilash
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.last_name = form.cleaned_data.get('last_name', request.user.last_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save(update_fields=['first_name', 'last_name', 'email'])
            form.save()
            messages.success(request, 'Profil muvaffaqiyatli yangilandi.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Iltimos, xatolarni to\'g\'rilang.')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileForm(instance=profile, initial=initial)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
