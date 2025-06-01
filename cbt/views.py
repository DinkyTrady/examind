from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
import json

from .models import Exam, Question, StudentAnswer


@login_required
def exam_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Check if exam has started
    if exam.date_start and exam.date_start > timezone.now():
        messages.error(request, "Ujian belum dimulai.")
        return redirect("cbt:exam_all")

    # Check if student has already completed the exam
    has_attempt = StudentAnswer.objects.filter(
        student=request.user, question__exam=exam
    ).exists()
    if has_attempt:
        messages.info(request, "Anda sudah mengerjakan ujian ini.")
        return redirect("cbt:exam_result", exam_id=exam_id)

    questions = exam.questions.order_by("order")
    total_questions = questions.count()

    question_number = int(request.GET.get("question", 1))
    if question_number < 1 or question_number > total_questions:
        question_number = 1

    current_question = questions[question_number - 1]

    # Get student answers efficiently using select_related
    student_answers = StudentAnswer.objects.select_related("question").filter(
        student=request.user, question__exam=exam
    )

    # Create hash map for O(1) lookup
    student_answers_map = {ans.question.order: ans for ans in student_answers}
    answered_questions = list(student_answers_map.keys())
    answered_count = len(answered_questions)
    unanswered_count = total_questions - answered_count

    # Get current question's selected answer
    current_answer = student_answers_map.get(current_question.order)
    selected_option = current_answer.selected_option if current_answer else None

    progress_percentage = (
        (answered_count / total_questions) * 100 if total_questions > 0 else 0
    )

    # Timer logic
    start_time = request.session.get(f"exam_{exam_id}_start_time")
    if not start_time:
        start_time = timezone.now()
        request.session[f"exam_{exam_id}_start_time"] = start_time.isoformat()
    else:
        start_time = timezone.datetime.fromisoformat(start_time)

    time_elapsed = timezone.now() - start_time
    time_remaining = timedelta(minutes=exam.duration) - time_elapsed
    time_remaining_seconds = max(0, int(time_remaining.total_seconds()))

    # Format time remaining for display
    hours = time_remaining_seconds // 3600
    minutes = (time_remaining_seconds % 3600) // 60
    seconds = time_remaining_seconds % 60
    time_remaining_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    context = {
        "exam": exam,
        "current_question": current_question,
        "current_question_number": question_number,
        "total_questions": total_questions,
        "question_numbers": list(range(1, total_questions + 1)),
        "answered_questions": answered_questions,
        "answered_count": answered_count,
        "unanswered_count": unanswered_count,
        "progress_percentage": progress_percentage,
        "time_remaining": time_remaining_str,
        "time_remaining_seconds": time_remaining_seconds,
        "question_ids": list(questions.values_list("id", flat=True)),
        "current_index": question_number - 1,
        "has_next": question_number < total_questions,
        "has_previous": question_number > 1,
        "selected_option": selected_option,
        "user_answers": {
            order: ans.selected_option
            for order, ans in student_answers_map.items()
            if ans.selected_option
        },
        "exam_id": exam.id,
    }
    return render(request, "siswa/exam.html", context)


@login_required
@require_POST
def save_answer(request):
    question_id = request.POST.get("question_id")
    selected_option = request.POST.get("answer")  # This should be 'A', 'B', 'C', or 'D'
    question = get_object_or_404(Question, id=question_id)

    # Validate selected option
    if selected_option not in ["A", "B", "C", "D"]:
        return JsonResponse({"success": False, "error": "Invalid option"})

    student_answer, created = StudentAnswer.objects.get_or_create(
        student=request.user,
        question=question,
        defaults={"selected_option": selected_option},
    )
    if not created:
        student_answer.selected_option = selected_option
        student_answer.save()

    return JsonResponse({"success": True})


@login_required
@require_POST
@csrf_exempt  # optional: hanya untuk testing jika CSRF error, sebaiknya dihapus nanti
def mark_review(request):
    try:
        data = json.loads(request.body)
        question_id = data.get("question_id")
        mark = data.get("mark", True)

        student_answer, created = StudentAnswer.objects.get_or_create(
            student=request.user,
            question_id=question_id,
            defaults={"marked_for_review": mark},
        )
        if not created:
            student_answer.marked_for_review = mark
            student_answer.save()

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@require_POST
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    try:
        # Calculate final score
        student_answers = StudentAnswer.objects.filter(
            student=request.user, question__exam=exam
        )

        total_score = 0
        max_score = 0
        correct_answers = 0

        for answer in student_answers:
            max_score += answer.question.points
            if answer.selected_option and answer.is_correct():
                total_score += answer.question.points
                correct_answers += 1

        # Store exam completion in session
        request.session[f"exam_{exam_id}_completed"] = True
        request.session[f"exam_{exam_id}_score"] = total_score
        request.session[f"exam_{exam_id}_max_score"] = max_score
        request.session[f"exam_{exam_id}_correct_answers"] = correct_answers

        # Clear start time
        if f"exam_{exam_id}_start_time" in request.session:
            del request.session[f"exam_{exam_id}_start_time"]

        return JsonResponse(
            {
                "success": True,
                "score": total_score,
                "max_score": max_score,
                "correct_answers": correct_answers,
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def exam_all(request):
    exams = Exam.objects.all()
    # Annotate each exam with whether the student has attempted it
    exam_ids_with_attempt = set(
        StudentAnswer.objects.filter(student=request.user).values_list(
            "question__exam_id", flat=True
        )
    )
    for exam in exams:
        exam.has_attempt = exam.id in exam_ids_with_attempt
    return render(request, "exam_list.html", {"exams": exams})


@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student_answers = (
        StudentAnswer.objects.filter(student=request.user, question__exam=exam)
        .select_related("question")
        .order_by("question__order")
    )

    total_score = 0
    max_score = 0
    correct_answers = 0

    for answer in student_answers:
        max_score += answer.question.points
        if answer.selected_option and answer.is_correct():
            total_score += answer.question.points
            correct_answers += 1

    # Calculate percentage
    percentage = (
        round((correct_answers / exam.get_total_questions() * 100), 2)
        if exam.get_total_questions() > 0
        else 0
    )

    context = {
        "exam": exam,
        "total_score": total_score,
        "max_score": max_score,
        "answers": student_answers,
        "percentage": percentage,
    }
    return render(request, "exam_result.html", context)
