from django.db import models
from django .conf import settings

# Create your models here.
class Attendance(models.Model):
    attend_at = models.DateTimeField()
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

