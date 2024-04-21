from django.db import models

# Create your models here.

class Person(models.Model):
    identification = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    birthdate = models.DateField()
    level = models.IntegerField(default=0)

    class Meta():
        ordering = ["-level"]

    def __str__(self):
        return "{} {} {} {}".format(self.id, self.identification, self.name, self.level)
