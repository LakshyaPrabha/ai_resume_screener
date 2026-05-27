from django.contrib import admin
from .models import ResumeScreen

@admin.register(ResumeScreen)
class ResumeScreenAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_title', 'ats_score', 'created_at']
    list_filter = ['ats_score', 'created_at']
    search_fields = ['user__username', 'job_title']
