import uuid
from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # NOQA
from rest_framework_api_key.models import APIKey


User = get_user_model()


class Application(models.Model):
    created = models.DateTimeField(
        default=timezone.now,
    )
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="applications",
        verbose_name=_("owner"),
    )
    id = models.CharField(
        max_length=255,
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        null=True,
        blank=True,
    )
    domain = models.CharField(
        max_length=255,
        verbose_name=_("domain"),
        unique=True,
    )
    apikeys = models.ManyToManyField(APIKey, through="ApplicationKey")

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_from_request_headers(cls, request):
        application_id = request.META.get("HTTP_X_APPLICATION", None)
        if application_id is None:
            application_id = request.headers.get("X-Application", None)
        application = cls.objects.filter(id=application_id).first()
        return application


class ApplicationKey(models.Model):
    application = models.ForeignKey(
        Application,
        related_name="api_keys",
        on_delete=models.CASCADE,
    )
    key = models.ForeignKey(
        APIKey,
        related_name="applications",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Aplication API Key"
        verbose_name_plural = "Aplication API Keys"
        unique_together = ("application", "key")

    def __str__(self) -> str:
        return f"{self.application}: {self.key}"
