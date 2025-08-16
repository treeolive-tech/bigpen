import json
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.http import HttpResponseNotAllowed, JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from .forms import EmailUsForm
from .models import EmailAddress, PhoneAddress, PhysicalAddress, SocialMediaAddress
from .serializers import (
    EmailAddressSerializer,
    PhoneAddressSerializer,
    PhysicalAddressSerializer,
    SocialMediaAddressSerializer,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class EmailUsView(View):
    def get(self, request):
        return HttpResponseNotAllowed(["POST"])

    def post(self, request):
        try:
            # Parse JSON data only
            try:
                json_data = json.loads(request.body)
                form = EmailUsForm(json_data)
            except json.JSONDecodeError:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid JSON data.",
                    },
                    status=400,
                )

            if not form.is_valid():
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Please correct the errors below.",
                        "errors": form.errors,
                    },
                    status=400,
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

            return JsonResponse(
                {
                    "success": True,
                    "message": "Thank you for your message! We will get back to you soon.",
                }
            )

        except Exception as e:
            logger.error(f"Error sending contact email: {str(e)}")
            return JsonResponse(
                {
                    "success": False,
                    "message": "There was an error sending your message. Please try again later.",
                },
                status=500,
            )


class EmailAddressViewSet(ReadOnlyModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_primary"]


class PhoneAddressViewSet(ReadOnlyModelViewSet):
    queryset = PhoneAddress.objects.all()
    serializer_class = PhoneAddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_primary", "use_for_whatsapp", "is_active"]


class PhysicalAddressViewSet(ReadOnlyModelViewSet):
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalAddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["use_in_contact_form", "is_active"]


class SocialMediaAddressViewSet(ReadOnlyModelViewSet):
    queryset = SocialMediaAddress.objects.all()
    serializer_class = SocialMediaAddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active"]
