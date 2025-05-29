from django.contrib import admin
from .models import Siswa, User
from .forms import SiswaCreationForm


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    ordering = ["email"]
    list_display = ["email", "username", "full_name", "is_staff"]


admin.site.register(User, UserAdmin)


class SiswaAdmin(admin.ModelAdmin):
    form = SiswaCreationForm
    list_display = (
        "nis",
        "username",
        "full_name",
        "email",
    )  # sesuaikan dengan method di model Siswa


admin.site.register(Siswa, SiswaAdmin)
