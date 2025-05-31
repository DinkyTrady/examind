from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
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
def user_report(request: HttpRequest):
    if request.user.role == "siswa":
        messages.info(request, "This feature is under development.")
        return redirect("account:siswa_dashboard")
    elif request.user.role == "guru":
        messages.info(request, "This feature is under development.")
        return redirect("account:guru_dashboard")
    else:
        messages.error(request, "Akun tidak terdaftar sebagai Siswa atau Guru.")
        return redirect("account:login_view")
