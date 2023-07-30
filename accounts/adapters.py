from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_email_confirmation_required(self, request, email):
        # Disable email confirmation for social logins
        return False