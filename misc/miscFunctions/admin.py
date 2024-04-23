from django.contrib import admin
from .models import Person, TRM, Inflation, Food, FoodEntry, FoodRatio, Animal

admin.site.register(Person)
admin.site.register(TRM)
admin.site.register(Inflation)
admin.site.register(Animal)
admin.site.register(Food)
admin.site.register(FoodRatio)
admin.site.register(FoodEntry)
