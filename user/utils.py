# user\utils.py

import random
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

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


# FOR KARIBU MAIL
def send_welcome_email(user, dashboard_url, community_url, support_email, help_center_url, unsubscribe_url):
    subject = "Welcome to AiCE Community 🎉"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@aice.community")
    to = [user.email]

    # Optional: plain-text fallback for clients that block HTML
    text_content = f"""
Hi {user.first_name or 'there'},

Welcome to AiCE Community!

Vision: Train 200 million Africans in Software Engineering by 2040.
Mission: Build world-class African software engineers grounded in Ubuntu and cultural pride.

Your 12-Month Journey: Foundation → Python/MySQL → Web Basics → React → Figma → Next.js → Django → React Native → Portfolio.

Next steps:
1) Open your dashboard: {dashboard_url}
2) Join the community: {community_url}

Need help? {support_email}
Unsubscribe: {unsubscribe_url}

Karibu AiCE!
"""

    # Load the HTML above into a Python triple-quoted string (or keep it as a separate template and render with Django templates)
    with open('karibu_aice.html', 'r', encoding='utf-8') as my_file:
        html_content = my_file.read()
    

    # If not using Django templates, you can do simple replacements:
    html_content = (html_content
        .replace("{{ first_name|default:\"there\" }}", user.first_name or "there")
        .replace("{{ dashboard_url }}", dashboard_url)
        .replace("{{ community_url }}", community_url)
        .replace("{{ support_email }}", support_email)
        .replace("{{ help_center_url }}", help_center_url)
        .replace("{{ unsubscribe_url }}", unsubscribe_url)
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
