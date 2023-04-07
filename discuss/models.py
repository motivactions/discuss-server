import uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from coreplus import markdown
from coreplus.profanity.extras import ProfanityFilter
from coreplus.utils.models.models import TimeStampedModel
from apps.models import Application

User = get_user_model()


class DiscussManager(TreeManager):
    def __init__(self, *args, **kwargs):
        self.hide_blocked_user = kwargs.pop("hide_blocked_user", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.hide_blocked_user:
            return super().get_queryset().filter(user__is_active=True)
        else:
            return super().get_queryset()

    def get(self, *args, **kwargs):
        if self.hide_blocked_user:
            kwargs["user__is_active"] = True
        return super().get(*args, **kwargs)


class Discuss(TimeStampedModel, MPTTModel):
    id = models.CharField(
        max_length=255,
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    application = models.ForeignKey(
        Application,
        related_name="discussions",
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.CharField(
        max_length=54,
        blank=True,
        null=True,
        help_text=_("Commented object id."),
        db_index=True,
    )
    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text=_("Discuss can have a hierarchy, totally optional."),
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        related_name="discuss",
        on_delete=models.CASCADE,
        db_index=True,
    )
    content = models.TextField(
        verbose_name=_("Content"),
    )
    content_html = models.TextField(
        editable=False,
        verbose_name=_("Content HTML"),
    )
    reaction = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("reaction"),
        help_text=_('JSON fields contains {"like": 1, "love":2, "flap":3}'),
    )
    flag = models.JSONField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("flag"),
        help_text=_('JSON fields contains {"spam": 1, "hoax":2, "bullying":3}'),
    )
    objects = DiscussManager()
    all_objects = DiscussManager(hide_blocked_user=False)

    class Meta:
        verbose_name = _("Discuss")
        verbose_name_plural = _("Discuss")

    def __str__(self):
        return f"{self.object_id} comment #{self.id}"

    @property
    def opts(self):
        return self.__class__._meta

    @property
    def children_count(self):
        return self.get_children().count()

    @property
    def descendant_count(self):
        return self.get_descendant_count()

    def reactions(self):
        """Get reactions from reaction service"""
        return []

    def add_reaction(self, user, value):
        return {}

    def remove_reaction(self, user):
        return {}

    def add_flag(self, value):
        return {}

    def remove_flag(self, user):
        return {}

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent discuss cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def delete(self, descendants=True, *args, **kwargs):
        """Remove discuss objects include descendants"""
        if descendants:
            descendants = self.get_descendants(include_self=False)
            descendants.delete()
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        If parent is available then set parent behaviour to children
        Apply profanity filter to content
        Parse content to content_html
        """
        if self.parent:
            self.object_id = self.parent.object_id
            self.application = self.parent.application

        self.content = ProfanityFilter().censor(self.content)
        self.content_html = markdown.parse(self.content)
        return super().save(*args, **kwargs)
