from django.contrib import admin
from .models import Siswa, Guru


# Register Siswa here.
class SiswaAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "nis", "kelas")
    search_fields = ("nama", "nis")


admin.site.register(Siswa, SiswaAdmin)


# Register Guru here.
class GuruAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "nip")
    search_fields = ("nama", "nip")


admin.site.register(Guru, GuruAdmin)
