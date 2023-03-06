from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    is_district_user = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_accounts'


class DistrictUser(models.Model):
    ALAPPUZHA = 'AL'
    ERNAKULAM = 'ER'
    IDUKKI = 'ID'
    KANNUR = 'KN'
    KASARGOD = 'KS'
    KOLLAM = 'KL'
    KOTTAYAM = 'KT'
    KOZHIKODE = 'KZ'
    MALAPPURAM = 'ML'
    PALAKKAD = 'PL'
    PATHANAMTHITTA = 'PT'
    THIRUVANANTHAPURAM = 'TV'
    THRISSUR = 'TS'
    WAYANAD = 'WA'

    DISTRICT_CHOICES = [
        (ALAPPUZHA, 'Alappuza'),
        (ERNAKULAM, 'Ernakulam'),
        (IDUKKI, 'Idukki'),
        (KANNUR, 'Kannur'),
        (KASARGOD, 'Kasargod'),
        (KOLLAM, 'Kollam'),
        (KOTTAYAM, 'Kottayam'),
        (KOZHIKODE, 'Kozhikode'),
        (MALAPPURAM, 'Malappuram'),
        (PALAKKAD, 'Palakkad'),
        (PATHANAMTHITTA, 'Pathanamthitta'),
        (THIRUVANANTHAPURAM, 'Thiruvananthapuram'),
        (THRISSUR, 'Thrissur'),
        (WAYANAD, 'Wayanad')
    ]
    district = models.CharField(max_length=2, choices=DISTRICT_CHOICES)

    class Meta:
        db_table = 'district_users'


class Token(models.Model):
    blacklistedtoken = models.CharField(max_length=300)
    
    class Meta:
        db_table = 'token'