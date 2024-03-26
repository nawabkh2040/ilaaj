from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
# from background_task import background
from home.models import CustomUser

# @background(schedule=0)  # Run the task immediately
def send_activation_email(user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        subject = "Email Verification by Treat Now"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        current_site = get_current_site(request)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        context_email = {
            'name': user.name,
            'domain': current_site.domain,
            'uidb64': uidb64,
            'token': token,
        }
        message = render_to_string('doctor/email_confirmation.html', context_email)
        send_mail(subject, message, from_email, to_list, fail_silently=True)
    except CustomUser.DoesNotExist:
        pass
