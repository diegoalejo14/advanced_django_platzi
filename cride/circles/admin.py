"""Circles Admin."""

# Django
from django.contrib import admin

# Model
from cride.circles.models import Circle

# Define Admin Circle Info in django platform


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle admin."""
    list_display = ('slug_name', 'name', 'is_public', 'verified', 'is_limited')
    search_fields = ('slug_name', 'name')
    list_filter = ('is_public', 'verified', 'is_limited')
