from django.contrib import admin
from cbt.models import Exam, Question, Option, StudentAnswer

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(StudentAnswer)

