from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

# Create your views here.

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            # Save to database
            ContactMessage.objects.create(name=name, email=email, message=message)

            # Send email to admin
            subject = f"New Contact Message from {name}"
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.EMAIL_HOST_USER]  # Send to admin email

            try:
                send_mail(subject, email_message, from_email, recipient_list)
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, "Message saved, but failed to send email notification.")
        else:
            messages.error(request, "Please fill in all fields.")
            
    return redirect('userhtml') # Redirect back to user dashboard
