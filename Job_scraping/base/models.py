from tkinter.tix import Tree
from django.db import models

# Create your models here.
class Job(models.Model):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    work_address = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    detail_link = models.CharField(max_length=100, unique=True)