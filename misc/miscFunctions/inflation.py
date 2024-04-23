from .models import Inflation
import random

def daily_update():
    create_inflation()

def calculate_inflation():
    value = random.randint(1, 10)
    decimals = random.randint(1, 10)
    return float(str(value) + "." + str(decimals))

def create_inflation():
    for y in range(2022,2024):
        for m in range(1,13):
            new_value = calculate_inflation()
            try:
                inf = Inflation.objects.get(month=m, year=y)
                inf.value = new_value
                inf.save()
            except:
                inflation, created = Inflation.objects.get_or_create(month=m, year=y, value=new_value)
                inflation.save()
