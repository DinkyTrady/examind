

# cbt/models.py
from django.db import models
from django.conf import settings

class Exam(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Durasi dalam menit")

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[('pilihan ganda', 'Pilihan Ganda')])
    points = models.IntegerField(default=1)
    order = models.IntegerField(help_text="Urutan soal dalam ujian")

    def __str__(self):
        return f"Soal {self.order}: {self.question_text[:50]}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_label = models.CharField(max_length=1)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_label}. {self.option_text}"


class StudentAnswer(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    marked_for_review = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - Soal {self.question.order}"