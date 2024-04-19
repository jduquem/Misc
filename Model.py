class person(models.Model):
    identification = models.ForeignKey(on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    birthdate = models.DateTimeField(null=True)