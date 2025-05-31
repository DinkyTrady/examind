from django import forms
from django.contrib.auth import get_user_model

from .models import Guru, Siswa

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["full_name", "username", "email", "password", "role"]

    field_order = ["full_name", "username" "email", "password", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        if commit:
            user.save()
        return user


class SiswaCreationForm(forms.ModelForm):
    full_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    # role = forms.ChoiceField(choices=[("siswa", "Siswa")])
    is_active = forms.BooleanField(initial=True)

    class Meta:
        model = Siswa
        fields = ["nis", "kelas"]  # Field khusus Siswa, jika ada

    field_order = [
        "nis",
        "kelas",
        "full_name",
        "username",
        "email",
        "password",
        "role",
        "is_active",
    ]

    def save(self, commit=True):
        user = User.objects.create_user(
            full_name=self.cleaned_data["full_name"],
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        siswa = super().save(commit=False)
        siswa.user = user
        if commit:
            siswa.save()
        return siswa


class SiswaChangeForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = ["kelas"]


class GuruCreationForm(forms.ModelForm):
    full_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    # role = forms.ChoiceField(choices=[("guru", "Guru")])
    is_active = forms.BooleanField(initial=True)

    class Meta:
        model = Guru
        fields = ["nip"]

    field_order = [
        "nip",
        "full_name",
        "username",
        "email",
        "password",
        "role",
        "is_active",
    ]

    def save(self, commit=True):
        user = User.objects.create_user(
            full_name=self.cleaned_data["full_name"],
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        guru = super().save(commit=False)
        guru.user = user
        if commit:
            guru.save()
        return guru


class GuruChangeForm(forms.ModelForm):
    class Meta:
        model = Guru
        fields = []
