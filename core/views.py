from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


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
