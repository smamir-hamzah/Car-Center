from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):
    """Redirect users after login based on role.

    - superuser+staff -> admin:index
    - assistants (is_assistant_executive) -> assistant_dashboard
    - others -> userhtml
    """

    def get_login_redirect_url(self, request):
        user = request.user
        if user is None:
            return super().get_login_redirect_url(request)

        if getattr(user, 'is_superuser', False) and getattr(user, 'is_staff', False):
            return reverse('admin:index')

        if getattr(user, 'is_assistant_executive', False):
            return reverse('assistant_dashboard')

        return reverse('userhtml')


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Social account adapter version of login redirect.

    some social flows call the social adapter for redirect decisions — keep
    behavior consistent with the account adapter.
    """

    def get_login_redirect_url(self, request, socialaccount=None):
        user = request.user
        if user is None:
            return super().get_login_redirect_url(request, socialaccount)

        if getattr(user, 'is_superuser', False) and getattr(user, 'is_staff', False):
            return reverse('admin:index')

        if getattr(user, 'is_assistant_executive', False):
            return reverse('assistant_dashboard')

        return reverse('userhtml')
