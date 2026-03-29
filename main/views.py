from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .models import Project, ContactMessage
def home(request):
    projects = Project.objects.all()[:6]
    return render(request, 'main/index.html', {'projects': projects})


def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'main/projects.html', {'projects': projects})

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        try:
            # ✅ Save to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            # ✅ Send message to your portfolio Gmail
            subject = f"📩 New Message from {name}"
            body = f"""
You have received a new message from your portfolio contact form:

-------------------------------------
👤 Name: {name}
📧 Email: {email}

💬 Message:
{message}
-------------------------------------
"""
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ["methuselaportifolio@gmail.com"],  # your Gmail
                fail_silently=False,
            )

            # ✅ Send auto-reply to sender
            send_mail(
                subject="✅ Thank you for reaching out!",
                message=f"Hi {name},\n\nThanks for contacting me! I’ve received your message and will get back to you soon.\n\nBest,\nMethusela Enoch",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

            # ✅ Display success popup
            messages.success(request, "✅ Your message has been sent successfully!")

        except BadHeaderError:
            messages.error(request, "❌ Invalid header found.")
        except Exception as e:
            messages.error(request, f"❌ Something went wrong: {e}")

        return redirect("contact")

    return render(request, "main/contact.html")


def contact_messages(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Forbidden')
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'main/contact_messages.html', {'messages_list': messages_list})
