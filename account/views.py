from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from cbt.models import Exam, Question

from .forms import ExamCreationForm, QuestionCreationForm
from .models import User


# Create your views here.
@csrf_exempt
def login_view(request: HttpRequest):
    # Check if someone are already authenticate with the server
    # and it will return depend on the role of the user
    if request.user.is_authenticated:
        username = request.user.username

        if hasattr(request.user, "siswa"):
            messages.warning(
                request,
                f"Anda telah login sebagai {username} otomatis redirect ke dashboard",
            )
            return redirect("account:siswa_dashboard")
        elif hasattr(request.user, "guru"):
            messages.warning(
                request,
                f"Anda telah login sebagai {username} otomatis redirect ke dashboard",
            )
            return redirect("account:guru_dashboard")
        else:
            logout(request)
            return render(
                request,
                "login.html",
                {"error": "Akun tidak terdaftar sebagai Siswa atau Guru."},
            )

    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.role == "siswa":
                return redirect("account:siswa_dashboard")
            elif request.user.role == "guru":
                return redirect("account:guru_dashboard")
            else:
                logout(request)
                error = "Akun tidak terdaftar sebagai Siswa atau Guru."
                return render(request, "login.html", {"error": error})
        else:
            error = "Username atau password salah."
            return render(request, "login.html", {"error": error})
    else:
        return render(request, "login.html", {"error": error})


@login_required(login_url="account:login")
def logout_view(request: HttpRequest):
    if request.method == "POST":
        full_name = request.user.full_name
        logout(request)
        messages.success(
            request,
            f"You have been successfully logged out. See you later, {full_name}!",
        )
        return redirect("homeweb:index")


@login_required(login_url="account:login")
def siswa_dashboard(request: HttpRequest):
    return render(request, "siswa/dashboard.html", {"user": request.user})


@login_required(login_url="account:login")
def guru_dashboard(request: HttpRequest):
    return render(request, "guru/dashboard.html", {"user": request.user})


@login_required(login_url="account:login")
def user_profile(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Only update username if it's different and not already taken
        if username and username != request.user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                request.user.username = username
                messages.success(request, "Username updated successfully.")

        # Update password if provided
        if password:
            request.user.set_password(password)
            request.user.save()
            # Re-authenticate the user to prevent logout
            user = authenticate(
                request, username=request.user.username, password=password
            )
            if user:
                login(request, user)
            messages.success(request, "Password berhasil diperbarui.")
            return redirect("account:user_profile")

        request.user.save()

    return render(request, "profile.html", {"user": request.user})


@login_required(login_url="account:login")
def guru_exam_list(request: HttpRequest):
    """List all exams created by the guru"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    exams = Exam.objects.all().order_by("-created_at")
    paginator = Paginator(exams, 10)  # Show 10 exams per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "guru/exam_list.html", {"page_obj": page_obj, "user": request.user}
    )


@login_required(login_url="account:login")
def guru_exam_create(request: HttpRequest):
    """Create a new exam"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    if request.method == "POST":
        form = ExamCreationForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, f"Ujian '{exam.title}' berhasil dibuat!")
            return redirect("account:guru_exam_detail", exam_id=exam.id)
    else:
        form = ExamCreationForm()

    return render(
        request, "guru/exam_create.html", {"form": form, "user": request.user}
    )


@login_required(login_url="account:login")
def guru_exam_detail(request: HttpRequest, exam_id: int):
    """View exam details and questions"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.order_by("order")

    return render(
        request,
        "guru/exam_detail.html",
        {"exam": exam, "questions": questions, "user": request.user},
    )


@login_required(login_url="account:login")
def guru_exam_edit(request: HttpRequest, exam_id: int):
    """Edit an existing exam"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == "POST":
        form = ExamCreationForm(request.POST, instance=exam)
        if form.is_valid():
            exam = form.save()
            messages.success(request, f"Ujian '{exam.title}' berhasil diperbarui!")
            return redirect("account:guru_exam_detail", exam_id=exam.id)
    else:
        form = ExamCreationForm(instance=exam)

    return render(
        request,
        "guru/exam_edit.html",
        {"form": form, "exam": exam, "user": request.user},
    )


@login_required(login_url="account:login")
def guru_exam_delete(request: HttpRequest, exam_id: int):
    """Delete an exam"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == "POST":
        exam_title = exam.title
        exam.delete()
        messages.success(request, f"Ujian '{exam_title}' berhasil dihapus!")
        return redirect("account:guru_exam_list")

    return render(
        request, "guru/exam_delete.html", {"exam": exam, "user": request.user}
    )


@login_required(login_url="account:login")
def guru_question_create(request: HttpRequest, exam_id: int):
    """Create a new question for an exam"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == "POST":
        form = QuestionCreationForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, "Soal berhasil ditambahkan!")
            return redirect("account:guru_exam_detail", exam_id=exam.id)
    else:
        form = QuestionCreationForm()

    return render(
        request,
        "guru/question_create.html",
        {"form": form, "exam": exam, "user": request.user},
    )


@login_required(login_url="account:login")
def guru_question_edit(request: HttpRequest, question_id: int):
    """Edit an existing question"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    question = get_object_or_404(Question, id=question_id)
    exam = question.exam

    if request.method == "POST":
        form = QuestionCreationForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            messages.success(request, "Soal berhasil diperbarui!")
            return redirect("account:guru_exam_detail", exam_id=exam.id)
    else:
        form = QuestionCreationForm(instance=question)

    return render(
        request,
        "guru/question_edit.html",
        {"form": form, "question": question, "exam": exam, "user": request.user},
    )


@login_required(login_url="account:login")
def guru_question_delete(request: HttpRequest, question_id: int):
    """Delete a question"""
    if not hasattr(request.user, "guru"):
        messages.error(request, "Akses ditolak. Anda bukan guru.")
        return redirect("account:login")

    question = get_object_or_404(Question, id=question_id)
    exam = question.exam

    if request.method == "POST":
        question.delete()
        messages.success(request, "Soal berhasil dihapus!")
        return redirect("account:guru_exam_detail", exam_id=exam.id)

    return render(
        request,
        "guru/question_delete.html",
        {"question": question, "exam": exam, "user": request.user},
    )
