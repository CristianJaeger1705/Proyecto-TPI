from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def populate_user_profile(request, user, **kwargs):
    # Datos que devuelve Google
    extra_data = user.socialaccount_set.filter(provider='google')[0].extra_data
    
    user.first_name = extra_data.get("given_name", "")
    user.last_name = extra_data.get("family_name", "")
    user.save()
