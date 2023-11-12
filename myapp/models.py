from django.db import models
from django.contrib.auth.models import User
class Schedule(models.Model):
    Day = models.CharField(max_length=50)
    Teacher = models.CharField(max_length=50)
    Period1 = models.CharField(max_length=50)
    Period2 = models.CharField(max_length=50)
    Period3 = models.CharField(max_length=50)
    Period4 = models.CharField(max_length=50)
    Period5 = models.CharField(max_length=50)
    Period6 = models.CharField(max_length=50)
    Period7 = models.CharField(max_length=50)
class Students(models.Model):
    USN = models.CharField(max_length=20)
    Sec = models.CharField(max_length=10)
    Contact = models.CharField(max_length=15)
    Semester = models.CharField(max_length=3)
class Attendence(models.Model):
    Updatedby = models.CharField(max_length=20)
    USN = models.CharField(max_length=20)
    Status = models.CharField(max_length=20)
    Date = models.DateField()
class Faculty(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=20)
    consulting  = models.CharField(max_length=20,default="")
    def __str__(self):
        return (self.name.username)
class messagestable(models.Model):
    From = models.CharField(max_length=20)
    To = models.CharField(max_length=20)
    Reason = models.CharField(max_length=20)
    Message = models.CharField(max_length=200)
    Status =  models.CharField(max_length=20)
class Tasks(models.Model):
    From = models.CharField(max_length=20)
    To = models.CharField(max_length=20)
    Reason = models.CharField(max_length=20)
    Message = models.CharField(max_length=200)
    Status =  models.CharField(max_length=20)
class Notification(models.Model):
    By = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
class Subjects(models.Model):
    Subjectcode = models.CharField(max_length=10)
    Semester = models.CharField(max_length=10)
class Marks(models.Model):
    USN = models.CharField(max_length=10)
    SubjectName = models.CharField(max_length=20)
    Internal = models.CharField(max_length=10)
    Input = models.BooleanField(default=True)
    Score = models.CharField(max_length=10)

