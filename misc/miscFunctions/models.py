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

class Inflation(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    value = models.FloatField()
    
    def __str__(self):
        return "id:{} - date:{} - month {} - value:{}".format(self.id, self.year, self.month, self.value)


class TRM(models.Model):
    date = models.DateField()
    value = models.FloatField()
    
    class Meta():
        ordering = ["-date"]

    def __str__(self):
        return "id:{} - date:{} - value:{}".format(self.id, self.date, self.value)

class Animal(models.Model):
    name = models.CharField(max_length=20)
    species = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class FoodEntry(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal} {self.food} {self.quantity} {self.date}"
    
class FoodRatio(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity_per_day = models.PositiveIntegerField()
    start_date = models.DateField()
    finish_date = models.DateField()
    
    def __str__(self):
        return f"{self.animal} {self.food} {self.quantity_per_day} {self.timestamp}"