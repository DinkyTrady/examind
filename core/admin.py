from django.contrib import admin
from .models import Siswa, Guru, Exam, Question, Option, StudentAnswer

# Admin untuk Siswa
class SiswaAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "nis", "kelas")
    search_fields = ("nama", "nis")

admin.site.register(Siswa, SiswaAdmin)

# Admin untuk Guru
class GuruAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "nip")
    search_fields = ("nama", "nip")

admin.site.register(Guru, GuruAdmin)

# Admin untuk Exam
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subject", "duration")
    search_fields = ("title", "subject")

# Admin untuk Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "exam", "order", "question_type", "points")
    list_filter = ("exam", "question_type")
    search_fields = ("question_text",)

# Admin untuk Option
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "option_label", "option_text", "is_correct")

# Admin untuk StudentAnswer
@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "question", "selected_option", "marked_for_review")
