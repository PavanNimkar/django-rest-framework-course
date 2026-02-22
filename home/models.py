from django.db import models


# Create your models here.


class Role(models.Model):
    role_name = models.CharField(max_length=10)

    def __str__(self):
        return self.role_name


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE)
