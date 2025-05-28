from django.db import models


# Create your models here.
class Siswa(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    nis = models.CharField(max_length=20, unique=True)
    kelas = models.CharField(max_length=10)


class Guru(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    nip = models.CharField(max_length=20, unique=True)
