from .forms import ExamForm  # kita buat di bawah
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, Question
from .forms import QuestionForm, OptionFormSet


@staff_member_required
def create_exam_with_question(request):
    print(">>> VIEW DIPANGGIL")
    if request.method == "POST":
        exam_form = ExamForm(request.POST)
        q_form = QuestionForm(request.POST)
        formset = OptionFormSet(request.POST)

        if exam_form.is_valid() and q_form.is_valid() and formset.is_valid():
            exam = exam_form.save()
            
            question = q_form.save(commit=False)
            question.exam = exam
            question.save()

            formset.instance = question
            formset.save()

            return redirect("cbt:edit_exam", exam_id=exam.id)  # arahkan ke halaman edit kalau ada
    else:
        exam_form = ExamForm()
        q_form = QuestionForm()
        formset = OptionFormSet()

    return render(
        request,
        "admin/create_cbt.html",
        {
            "exam_form": exam_form,
            "q_form": q_form,
            "formset": formset,
        }
    )
