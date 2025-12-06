from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class GoogleAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        user.first_name = data.get("given_name", "")
        user.last_name = data.get("family_name", "")
        if not sociallogin.is_existing:
            user.rol = "candidato"
        user.verificado = False

        return user
