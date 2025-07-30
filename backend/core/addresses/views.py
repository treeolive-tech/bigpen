import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import EmailUsForm
from .models import EmailAddress

logger = logging.getLogger(__name__)


class EmailUsAPIView(APIView):
    def post(self, request):
        try:
            # Use Django form for validation
            form = EmailUsForm(request.data)
            if not form.is_valid():
                return Response(
                    {
                        "success": False,
                        "message": "Please correct the errors below.",
                        "errors": form.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Extract validated data
            sender_name = form.cleaned_data["name"]
            sender_email = form.cleaned_data["email"]
            sender_subject = form.cleaned_data["subject"]
            sender_message = form.cleaned_data["message"]

            # Get recipient email
            recipient_email = None
            try:
                # Attempt to get the primary contact email from the EmailAddress model
                if (
                    EmailAddress._meta.db_table
                    in connection.introspection.table_names()
                ):
                    contact_email_obj = EmailAddress.objects.filter(
                        is_primary=True
                    ).first()
                    if contact_email_obj:
                        recipient_email = contact_email_obj.email

                # The DEFAULT_FROM_EMAIL sends the email, but note that we're getting the email address of the one who is actually sending from the EmailUsForm.
                # If there is no primary email for receiving, fallback to the DEFAULT_FROM_EMAIL which will now not only send the email but also receive it.
                if not recipient_email:
                    recipient_email = getattr(
                        settings, "DEFAULT_FROM_EMAIL", "admin@example.com"
                    )
            except Exception as e:
                logger.error(f"Error getting recipient email: {str(e)}")

            # Prepare email context
            email_context = {
                "name": sender_name,
                "email": sender_email,
                "subject": sender_subject,
                "message": sender_message,
                "url": request.build_absolute_uri("/"),
            }

            # Render email templates
            text_content = render_to_string("addresses/email-us.txt", email_context)
            html_content = render_to_string("addresses/email-us.html", email_context)

            # Send email
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")

            msg = EmailMultiAlternatives(
                f"Contact Form: {sender_subject}",
                text_content,
                from_email,
                [recipient_email],
                reply_to=[sender_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response(
                {
                    "success": True,
                    "message": "Thank you for your message! We will get back to you soon.",
                }
            )

        except Exception as e:
            logger.error(f"Error sending contact email: {str(e)}")
            return Response(
                {
                    "success": False,
                    "message": "There was an error sending your message. Please try again later.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
