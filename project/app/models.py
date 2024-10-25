from django.db import models
from django.contrib.auth.models import AbstractUser,User
from .manager import CustomManager
# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email_address", unique=True)
    position = models.CharField(
        "Position", max_length=122)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomManager()

    def __str__(self):
        return self.email


class EventInformation(models.Model):
    eventname = models.CharField(max_length=122)
    eventorganizer = models.CharField(max_length=122)
    eventday = models.CharField(max_length=122)
    eventdate = models.CharField(max_length=122)
    eventtime = models.CharField(max_length=122)
    eventabout = models.TextField(max_length=1000)
    eventfile = models.FileField(upload_to='files/')
    fileurl=models.CharField(max_length=122)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


class FormData(models.Model):
    data = models.JSONField()
    user = models.ForeignKey(CustomUser, name="customuser", on_delete=models.CASCADE)
    event = models.ForeignKey(EventInformation, name="event", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.data)

class DraftModel(models.Model):
    data=models.JSONField()
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,name="user")
    event=models.ForeignKey(EventInformation, name="event", on_delete=models.CASCADE,null=True)
