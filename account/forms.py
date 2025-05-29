from django import forms
from django.contrib.auth import get_user_model
from .models import Siswa

User = get_user_model()


class SiswaCreationForm(forms.ModelForm):
    full_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[("siswa", "Siswa")])
    is_active = forms.BooleanField(initial=True)

    class Meta:
        model = Siswa
        fields = ["nis", "full_name", "email"]  # Field khusus Siswa, jika ada

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
