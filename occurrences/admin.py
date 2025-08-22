from django.contrib import admin

from django.contrib import admin
from .models import Occurrence

@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "severity", "category", "reported_by", "occurred_at", "created_at")
    list_filter = ("status", "severity", "category", "reported_by")
    search_fields = ("title", "description", "category", "reported_by__username")
