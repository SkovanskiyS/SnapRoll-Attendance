from django.db import models


class Students(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    enroll_number = models.CharField(default='0', max_length=100)
    faculty = models.CharField(max_length=50)
    semester = models.IntegerField()
    section = models.IntegerField()
    face = models.ImageField(null=True, blank=True, upload_to='media/faces')
