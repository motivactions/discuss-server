from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Application, ApplicationKey


class ApplicationKeyInline(admin.TabularInline):
    model = ApplicationKey
    extra = 0


@admin.register(Application)
class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = ["id"]
    inlines = [ApplicationKeyInline]
