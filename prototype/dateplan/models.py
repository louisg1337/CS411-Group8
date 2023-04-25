from django.db import models

# Create your models here.from django.contrib.auth.models import User
from django.contrib.auth.models import User

class PlanContext(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weather = models.JSONField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    plan_date = models.DateField()

