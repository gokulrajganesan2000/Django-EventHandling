from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Events(models.Model):
    department=models.CharField(max_length=100,default=None)
    title=models.CharField(max_length=100)
    description=models.TextField()
    organizer=models.CharField(max_length=20)
    event_date=models.DateField()
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    url=models.CharField(max_length=200)
    poster=models.ImageField(default='default.jpg',upload_to='poster')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    date_posted=models.DateTimeField(default=timezone.now)
    requested_time=models.TimeField()
    purpose=models.CharField(max_length=100)
    is_principal_accepted=models.IntegerField(default=0)
    principal_comments=models.TextField(default='None')

    def __str__(self):
        return f'{self.title}'
