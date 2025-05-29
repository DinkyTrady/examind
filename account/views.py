from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login_view(request: HttpRequest):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if hasattr(user, "siswa"):
                return redirect("account:siswa_dashboard")
            elif hasattr(user, "guru"):
                return redirect("account:guru_dashboard")
            else:
                logout(request)
                error = "Akun tidak terdaftar sebagai Siswa atau Guru."
        else:
            error = "Username atau password salah."
            pass
    else:
        return render(request, "login.html", {"error": error})


@login_required
def logout_view(request: HttpRequest):
    if request.method == "POST":
        username = request.user.username if request.user.is_authenticated else "User"
        logout(request)
        messages.success(
            request, f"You have been successfully logged out. See you, {username}!"
        )
        return redirect("homeweb:index")


@login_required
def siswa_dashboard(request: HttpRequest):
    return render(request, "siswa/dashboard.html", {"user": request.user})
