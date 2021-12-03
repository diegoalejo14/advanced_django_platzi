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

    actions=['make_verified','make_unverified']


    def make_verified(self,request,queryset):
        """Make circle verify"""
        queryset.update(verified=True)
    make_verified.short_description='Make selected circles verify'


    def make_unverified(self,request,queryset):
        """Make circle reverse verify"""
        queryset.update(verified=False)
    make_unverified.short_description='Make selected circles reverse verify'
