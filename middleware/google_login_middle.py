from django.shortcuts import redirect
from django.urls import reverse, resolve


class SocialAuthMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        open_paths = [
           '/login/',
           '/social-auth/login/google-oauth2/',
        ]

        if request.path not in open_paths:

            print(request.path)

            if not request.user.is_authenticated:

                return redirect(reverse('social:begin', args=('google-oauth2',)))

        response = self.get_response(request)

        return response
