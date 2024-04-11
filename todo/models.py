from django.db import models
from django.contrib.auth.models import User
# Create your models here.
PRIORITY_CHOICES=[
    ('Regular', 'Regular'),
    ('Moderate', 'Moderate'),
    ('Important', 'Important'),
    ('Urgent', 'Urgent'),
    ('Very Urgent', 'Very Urgent'),
]

class PriorityChoices(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    date=models.DateField(auto_now_add = True)
    priority = models.CharField(choices=PRIORITY_CHOICES,max_length=20, default='Regular')

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username