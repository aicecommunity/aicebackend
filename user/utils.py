# user\utils.py

import random
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_code(user):
    code = generate_verification_code()
    user.verification_code = code
    user.code_expiry = timezone.now() + timedelta(minutes=10)
    user.save()

    subject = "AiCE Verification Code"
    from_email = "aicecommunity@gmail.com"
    to = [user.email]

    text_content = f"Your verification code is {code}. It will expire in 10 minutes."
   

    with open('email_code.html', 'r', encoding='utf-8') as my_file:
        html_content = my_file.read()
    
    html_content = html_content.format(
        first_name = user.first_name or '',
        code = code
    )

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()



def send_verification_code(user):
    code = generate_verification_code()
    user.verification_code = code
    user.code_expiry = timezone.now() + timedelta(minutes=10)
    user.save()

    subject = "AiCE Verification Code"
    from_email = "aicecommunity@gmail.com"
    to = [user.email]

    text_content = f"Your verification code is {code}. It will expire in 10 minutes."
   

    with open('email_code.html', 'r', encoding='utf-8') as my_file:
        html_content = my_file.read()
    
    html_content = html_content.format(
        first_name = user.first_name or '',
        code = code
    )

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()



