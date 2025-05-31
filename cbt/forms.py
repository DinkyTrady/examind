from django import forms
from .models import Exam, Question, Option
from django.forms import inlineformset_factory

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'subject', 'duration']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'points', 'order']

OptionFormSet = inlineformset_factory(Question, Option, fields=('option_label', 'option_text', 'is_correct'), extra=4, can_delete=True)
