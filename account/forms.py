from django import forms
from django.contrib.auth import get_user_model

from cbt.models import Exam, Question
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


class ExamCreationForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["title", "subject", "duration", "date_start"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Masukkan judul ujian"}
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Masukkan mata pelajaran",
                }
            ),
            "duration": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Durasi dalam menit"}
            ),
            "date_start": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if duration and duration <= 0:
            raise forms.ValidationError("Durasi harus lebih dari 0 menit.")
        return duration


class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
            "points",
        ]
        widgets = {
            "question_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Masukkan pertanyaan",
                }
            ),
            "option_a": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Pilihan A"}
            ),
            "option_b": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Pilihan B"}
            ),
            "option_c": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Pilihan C"}
            ),
            "option_d": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Pilihan D"}
            ),
            "correct_answer": forms.Select(attrs={"class": "form-control"}),
            "points": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Poin soal"}
            ),
        }

    def clean_points(self):
        points = self.cleaned_data.get("points")
        if points and points <= 0:
            raise forms.ValidationError("Poin soal harus lebih dari 0.")
        return points
