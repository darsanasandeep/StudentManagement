

from MySQLdb.constants.FLAG import UNIQUE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Course(models.Model):
    course = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=20, unique=True,default='TEMP_CODE')

class Subject(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)

class Teacher(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=timezone.now)
    first_name = models.CharField(max_length=50,default= timezone.now)
    last_name = models.CharField(max_length=50,default=timezone.now)
    phone = models.CharField(max_length=50,default=timezone.now)
    address = models.CharField(max_length=200,default=timezone.now)
    qualification = models.CharField(max_length=50,default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,default=timezone.now)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default= timezone.now)
    first_name = models.CharField(max_length=50,default= timezone.now)
    last_name = models.CharField(max_length=50,default= timezone.now)
    phone = models.CharField(max_length=50,default= timezone.now)
    address = models.CharField(max_length=200,default= timezone.now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Attendance(models.Model):
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(Attendance, related_name="records", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(("Present", "Present"), ("Absent", "Absent")))

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    mark = models.IntegerField()




