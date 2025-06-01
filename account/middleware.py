from django.http import HttpResponseRedirect
from django.urls import reverse


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is trying to access admin
        if request.path.startswith("/admin/") and request.user.is_authenticated:
            redirect_url = None

            # Check if user is a siswa - silent redirect
            if hasattr(request.user, "siswa"):
                redirect_url = reverse("account:siswa_dashboard")

            # Check if user is a guru - silent redirect
            elif hasattr(request.user, "guru"):
                redirect_url = reverse("account:guru_dashboard")

            # Redirect without any message
            if redirect_url:
                # Try to get the previous URL from session or HTTP_REFERER
                previous_url = request.session.get("last_page") or request.META.get(
                    "HTTP_REFERER"
                )
                if (
                    previous_url
                    and not previous_url.endswith("/admin/")
                    and "/admin/" not in previous_url
                ):
                    return HttpResponseRedirect(previous_url)
                else:
                    return HttpResponseRedirect(redirect_url)

        # Store current URL for future reference (excluding admin URLs)
        if not request.path.startswith("/admin/") and request.user.is_authenticated:
            request.session["last_page"] = request.get_full_path()

        response = self.get_response(request)
        return response
