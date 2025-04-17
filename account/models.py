from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import re
from datetime import timedelta
from django.utils import timezone

class UserManager(models.Manager):
    def create_user(self, phone, email=None, password=None, **extra_fields):
        phone = self.normalize_phone(phone)
        if not email:
            user = self.model(phone=phone, email=None, **extra_fields)
        else:
            email = self.normalize_email(email)
            user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(phone, email, password, **extra_fields)
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})
    @staticmethod
    def convert_persian_to_english(phone: str) -> str:
        persian_english_digits = dict({'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'})
        for persian, english in persian_english_digits.items():
            phone = str(phone.replace(persian, english))
        return phone
    @staticmethod
    def normalize_phone(phone: str):
        if not phone:
            raise ValueError('users must have a phone number! ')
        phone = UserManager.convert_persian_to_english(phone)
        phone = re.sub(r'\D', '', phone)
        if len(phone) == 11 and phone.startswith('09'):
            return phone
        else:
            raise ValueError('InValid phone Number! ')
    @staticmethod
    def normalize_email(email):
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email
class User(AbstractBaseUser):
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    @property
    def is_staff(self):
        return self.is_admin
    objects = UserManager()
    phone = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=11,
        verbose_name='Phone Number'
    )
    email = models.EmailField(unique=True, max_length=255, null=True, blank=True)
    is_email_verify = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.phone
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
class Otp(models.Model):
    code = models.SmallIntegerField()
    token = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def clean_otp():
        now = timezone.now()
        five_minutes = now - timedelta(minutes=5)

        Otp.objects.filter(created_at__lte=five_minutes).delete()

class MailCode(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    code = models.SmallIntegerField()

class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField()
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"zip-code:{self.zip_code} Address:{self.address[:50]}..."