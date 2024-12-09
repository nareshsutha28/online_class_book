from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import CustomUserManager


# Create your models here.
class User(AbstractUser):

    class UserRole(models.TextChoices):
        STUDENT = 'Student', 'Student'
        TEACHER = 'Teacher', 'Teacher'

    # Field declarations
    username = None
    email = models.EmailField(unique = True)
    age = models.PositiveIntegerField(null=True)
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=20, choices=UserRole.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    objects = CustomUserManager()

    def __str__(self):
      return "{}".format(self.email)


class TeacherProfile(models.Model):
   
   user = models.OneToOneField(User, related_name="teacher_profile", on_delete=models.CASCADE)
   subject = models.CharField(max_length=20)
