import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Affiliate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.country})"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('username', email)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('viewer', 'Viewer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True
    )
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['full_name', 'email']

    def __str__(self):
        return self.full_name or self.email

    def get_display_name(self):
        return self.full_name or self.email

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_staff_member(self):
        return self.role in ('admin', 'staff') or self.is_superuser
