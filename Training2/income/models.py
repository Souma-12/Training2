from datetime import date
from sre_constants import CATEGORY
from django.db import models
from authentication.models import User


class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY' , 'SALARY'),
        ('BUSINESS' , 'BUSINESS'),
        ('SIDE-HUSTLES' , 'SIDE-HUSTLES'),
        ('OTHERS' , 'OTHERS'),
    ]

    source = models.CharField(choices=SOURCE_OPTIONS, max_length=25)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255)
    description = models.CharField(choices=SOURCE_OPTIONS, max_length=25)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering= ['-date']

    def __str__(self):
        return str(self.owner)+'s income'
    
    
