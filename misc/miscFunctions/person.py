from django.db import transaction
from django.db.models.functions import Length
from .models import Person
import random, time
from faker import Faker

def create_identification():
    for _ in range(10):
        cedula = ''.join(str(random.randint(0,9)) for _ in range (10))
    return cedula

def save_person(person):
    try:
        filtered = Person.objects.filter(identification=person.identification)
        if len(filtered) == 0:
            user = Person(identification=person.identification, name=person.name, birthdate=person.birthdate)
            user.save()
            return 0
        else:
            filtered[0].level += 1
            filtered[0].save()
            return 1
    except:
        print('error')
        return 2

def create_persons(quantity):
    persons = []
    for _ in range(quantity):
        fake = Faker()
        identification = create_identification()
        name = fake.name()
        birthdate = fake.date_this_century()
        person = Person(identification=identification, name=name, birthdate=birthdate)
        persons.append(person)
    return persons

def save_multiple_persons(persons, save=True):
    leveled = 0
    created = 0
    retries = 100
    for _ in range(retries):
        try:
            with transaction.atomic():
                for person in persons:
                    try:
                        person_filtered = Person.objects.get(identification=person.identification)
                        person_filtered.level +=1
                        if person_filtered.level >= 10: person_filtered.level = 9
                        person_filtered.save()
                        leveled += 1
                    except:
                        if save:
                            person.save()
                            created += 1
                        pass
            break
        except Exception as e:
            print('waiting 1 {}'.format(str(e)))
            time.sleep(0.06)
    else:
        print('Database locked')
    return created, leveled

def create_and_save_persons_limit(limit):
    flag = 1
    retries = 100
    for _ in range(retries):
        try:
            if Person.objects.count() < limit:
                print("Add {} persons".format(limit - Person.objects.count()))
                while Person.objects.count() < limit:
                    persons_count = Person.objects.count()
                    left = limit - persons_count
                    if left < flag:
                        flag = limit - persons_count
                    created, leveled = save_multiple_persons(create_persons(flag))
                    print('Added {} - Leveled {} - Left {}'.format(created, leveled, left - flag))
                    flag *= 2
                    if flag > 1000: flag = 1000
            break
        except:
            print('waiting 2')
            time.sleep(0.06)
    else:
        print('Database locked')

def create_and_save_persons_count(count):
    created = 0
    leveled = 0
    errors = 0
    pending = count
    while created < count:
        persons = create_persons(pending)
        for p in persons:
            result = save_person(p)
            if result == 0:
                created += 1
            if result == 1:
                leveled +=1
            if result == 2:
                errors +=1
        pending = pending - created
    print('Loops:{}-Created:{}-Leveled:{}-Errors:{}'.format(created+leveled+errors,created,leveled,errors))

def level_persons(amount):
    print('Leveling {}'.format(amount))
    persons = create_persons(amount)
    created, leveled = save_multiple_persons(persons, False)
    print('Amount {} Leveled {}'.format(amount, leveled))

def job():
    print('Persons job')
    start = time.time()

    total_persons = Person.objects.count()
    cant = 100
    left = total_persons % cant
    if left > 0: cant = cant - left
    create_and_save_persons_limit(total_persons + cant)
    level_persons(int(total_persons * 0.0001))
    
    total_persons = Person.objects.count()
    level_0_persons = Person.objects.filter(level=0).count()
    leveled_persons = total_persons - level_0_persons
    print('Leveled={} - Level zero={} - Total={}'.format(leveled_persons, level_0_persons, total_persons))
    
    end = time.time()
    elapsed = (end - start)
    print('elapsed {}'.format(elapsed))
    