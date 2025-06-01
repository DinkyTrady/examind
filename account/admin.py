from django.contrib import admin

from .forms import GuruCreationForm, SiswaCreationForm, UserCreationForm
from .models import Guru, Siswa, User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    ordering = ["email"]
    list_display = ["email", "username", "full_name", "role", "is_staff", "is_active"]


admin.site.register(User, UserAdmin)


class SiswaAdmin(admin.ModelAdmin):
    form = SiswaCreationForm
    ordering = ["nis"]
    list_display = (
        "nis",
        "get_username",
        "get_full_name",
        "get_email",
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            from .forms import SiswaChangeForm

            return SiswaChangeForm
        else:
            return SiswaCreationForm

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return ("nis", "get_username", "get_full_name", "get_email")

        return ()

    def get_username(self, obj):
        return obj.user.username if obj else ""

    get_username.short_description = "Username"

    def get_full_name(self, obj):
        return obj.user.full_name if obj else ""

    get_full_name.short_description = "Full Name"

    def get_email(self, obj):
        return obj.user.email if obj else ""

    get_email.short_description = "Email"


admin.site.register(Siswa, SiswaAdmin)


class GuruAdmin(admin.ModelAdmin):
    form = GuruCreationForm
    ordering = ["nip"]
    list_display = ("nip", "get_username", "get_full_name", "get_email")

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            from .forms import GuruChangeForm

            return GuruChangeForm
        else:
            return GuruCreationForm

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return ("nip", "get_username", "get_full_name", "get_email")

        return ()

    def get_username(self, obj):
        return obj.user.username if obj else ""

    get_username.short_description = "Username"

    def get_full_name(self, obj):
        return obj.user.full_name if obj else ""

    get_full_name.short_description = "Full Name"

    def get_email(self, obj):
        return obj.user.email if obj else ""

    get_email.short_description = "Email"


admin.site.register(Guru, GuruAdmin)
