class Person(models.Model):
    identification = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    birthdate = models.DateTimeField()
    level = models.IntegerField()