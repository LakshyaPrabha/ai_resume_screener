from django.db import models
from django.contrib.auth.models import User


class ResumeScreen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='screens')
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    resume_text = models.TextField()
    ats_score = models.IntegerField(default=0)
    matched_skills = models.TextField(default='')   # comma separated
    missing_skills = models.TextField(default='')   # comma separated
    suggestions = models.TextField(default='')
    overall_feedback = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.job_title} ({self.ats_score}%)"

    def matched_skills_list(self):
        return [s.strip() for s in self.matched_skills.split(',') if s.strip()]

    def missing_skills_list(self):
        return [s.strip() for s in self.missing_skills.split(',') if s.strip()]

    def suggestions_list(self):
        return [s.strip() for s in self.suggestions.split('\n') if s.strip()]
