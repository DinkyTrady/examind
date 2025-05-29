from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
import json

from .models import Exam, Question, Option, StudentAnswer


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})


def logout(request):
    if request.method == "POST":
        username = request.user.username if request.user.is_authenticated else "User"
        logout(request)
        messages.success(
            request, f"You have been successfully logged out. See you, {username}!"
        )
        return redirect("core:logout")
    return redirect("core:dashboard")


def logout_success(request):
    return render(request, "logout.html")


@login_required
def dash_siswa(request):
    return render(request, 'siswa/dash_siswa.html')


@login_required
def exam_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.order_by('order')
    total_questions = questions.count()

    question_number = int(request.GET.get('question', 1))
    if question_number < 1 or question_number > total_questions:
        question_number = 1

    current_question = questions[question_number - 1]

    student_answers = StudentAnswer.objects.filter(student=request.user, question__exam=exam)
    answered_questions = student_answers.values_list('question__order', flat=True)
    answered_count = student_answers.count()
    unanswered_count = total_questions - answered_count
    progress_percentage = (answered_count / total_questions) * 100 if total_questions > 0 else 0

    start_time = request.session.get(f'exam_{exam_id}_start_time')
    if not start_time:
        start_time = timezone.now()
        request.session[f'exam_{exam_id}_start_time'] = str(start_time)
    else:
        start_time = timezone.datetime.fromisoformat(start_time)

    time_elapsed = timezone.now() - start_time
    time_remaining = timedelta(minutes=exam.duration) - time_elapsed
    time_remaining_seconds = int(time_remaining.total_seconds())
    time_remaining_str = str(time_remaining).split('.')[0]

    context = {
        'exam': exam,
        'current_question': current_question,
        'current_question_number': question_number,
        'total_questions': total_questions,
        'question_numbers': list(range(1, total_questions + 1)),
        'answered_questions': list(answered_questions),
        'answered_count': answered_count,
        'unanswered_count': unanswered_count,
        'progress_percentage': progress_percentage,
        'time_remaining': time_remaining_str,
        'time_remaining_seconds': time_remaining_seconds,
        'question_ids': list(questions.values_list('id', flat=True)),
        'current_index': question_number - 1,
        'user_answers': {
            ans.question.order: ans.selected_option.id
            for ans in student_answers if ans.selected_option
        },
           "exam_id": exam.id,
    }
    return render(request, 'siswa/exam.html', context)


@login_required
@require_POST
def save_answer(request):
    question_id = request.POST.get('question_id')
    option_id = request.POST.get('answer')
    question = get_object_or_404(Question, id=question_id)
    option = get_object_or_404(Option, id=option_id)

    student_answer, created = StudentAnswer.objects.get_or_create(
        student=request.user,
        question=question,
        defaults={'selected_option': option}
    )
    if not created:
        student_answer.selected_option = option
        student_answer.save()

    return JsonResponse({'success': True})


@login_required
@require_POST
@csrf_exempt  # optional: hanya untuk testing jika CSRF error, sebaiknya dihapus nanti
def mark_review(request):
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        mark = data.get('mark', True)

        student_answer, created = StudentAnswer.objects.get_or_create(
            student=request.user,
            question_id=question_id,
            defaults={'marked_for_review': mark}
        )
        if not created:
            student_answer.marked_for_review = mark
            student_answer.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def submit_exam(request):
    if request.method == 'POST':
        # Di sini Anda bisa menambahkan logika untuk menghitung nilai
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student_answers = StudentAnswer.objects.filter(student=request.user, question__exam=exam)
    total_score = 0
    max_score = 0

    for answer in student_answers:
        if answer.selected_option and answer.selected_option.is_correct:
            total_score += answer.question.points
        max_score += answer.question.points

    context = {
        'exam': exam,
        'total_score': total_score,
        'max_score': max_score,
    }
    return render(request, 'cbt/exam_result.html', context)
