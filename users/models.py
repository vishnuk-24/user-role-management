from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):

    class UserRole(models.TextChoices):
        STUDENT = 'student', 'Student'
        STAFF = 'staff', 'Staff'
        ADMIN = 'admin', 'Admin'
        EDITOR = 'editor', 'Editor'

    role = models.CharField(max_length=7, choices=UserRole.choices, default=UserRole.STUDENT)
    country = models.CharField(max_length=30)
    nationality = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
    
    @property
    def role_name(self):
        return self.get_role_display()
