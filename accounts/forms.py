from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ismingiz'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Familiyangiz'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email manzilingiz'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Foydalanuvchi nomi'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email allaqachon ro\'yxatdan o\'tgan.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu foydalanuvchi nomi band.')
        return username


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ismingiz'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Familiyangiz'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'phone', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O\'zingiz haqingizda'}),
            'phone': forms.TextInput(attrs={'placeholder': '+998 90 000 00 00'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'size'):
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Avatar fayli 5MB dan kichik bo\'lishi kerak.')
            valid_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(avatar, 'content_type') and avatar.content_type not in valid_types:
                raise forms.ValidationError('Faqat JPEG, PNG, GIF yoki WebP formatdagi rasm qabul qilinadi.')
        return avatar
