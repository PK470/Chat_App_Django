from django.db import models
from django.conf import settings
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# Create your models here.


class UserManager(BaseUserManager):
    """Manger for User"""

    def create_user(self, email,password=None, **extra_fields):
        """Create and return a `User` with an email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        #print(email)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """Create and return a `User` with superuser (admin) permissions."""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']