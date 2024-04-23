from django.db import transaction
from django.db.models.functions import Length
from .models import Person
import random, time
from faker import Faker

def create_identification():
    for _ in range(10):
        cedula = ''.join(str(random.randint(0,9)) for _ in range (10))
    return cedula

def create_single_person(person):
    try:
        filtered = Person.objects.filter(identification=person.identification)
        if len(filtered) == 0:
            user = Person(identification=person.identification, name=person.name, birthdate=person.birthdate)
            user.save()
            print('created')
            return 0
        else:
            filtered[0].level += 1
            filtered[0].save()
            print("leveled {}".format(filtered[0].level))
            return 1
    except:
        print('error')
        return 2

def create_person():
    try:
        fake = Faker()
        identification = create_identification()
        name = fake.name()
        birthdate = fake.date_this_century()
        
        filtered = Person.objects.filter(identification=identification)
        if len(filtered) == 0:
            user = Person(identification=identification, name=name, birthdate=birthdate)
            user.save()
            #print(Person.objects.count())
        else:
            filtered[0].level += 1
            filtered[0].save()
            print("level {}".format(filtered[0].level))

#        list_users()
    except Exception as e:
        print("error {}".format(str(e)))
        print("user not created {} {} {}".format(identification, name, birthdate))

def list_users():
    users = Person.objects.order_by('-id')[:10]
    for user in users:
        print("{} {} {} {} {}".format(user.id, user.identification, user.name, user.birthdate, user.level))

def create_multiple_persons(quantity):
    fake = Faker()
    persons = []
    for _ in range(quantity):
        identification = create_identification()
        name = fake.name()
        birthdate = fake.date_this_century()
        person = Person(identification=identification, name=name, birthdate=birthdate)
        persons.append(person)
    return persons

def save_persons(persons):
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
                        person_filtered.save()
                        leveled += 1
                    except:
                        person.save()
                        created += 1
            break
        except Exception as e:
            print('waiting 1 {}'.format(str(e)))
            time.sleep(0.06)
    else:
        print('Database locked')
    return created, leveled

def create_persons(limit):
    flag = 1
    retries = 100
    for _ in range(retries):
        try:
            if Person.objects.count() < limit:
                print("Add {} persons".format(limit - Person.objects.count()))
                while Person.objects.count() < limit:
                    left = limit - Person.objects.count()
                    if left < flag:
                        flag = limit - Person.objects.count()
                    created, leveled = save_persons(create_multiple_persons(flag))
                    print('Added {} - Leveled {} - Left {}'.format(created, leveled, left - flag))
                    flag *= 2
                    if flag > 1000: flag = 1000
            break
        except:
            print('waiting 2')
            time.sleep(0.06)
    else:
        print('Database locked')

def ap(limit=100):
    created = 0
    leveled = 0
    errors = 0
    pending = limit
    while created < limit:
        persons = create_multiple_persons(pending)
        for p in persons:
            result = create_single_person(p)
            if result == 0:
                created += 1
            if result == 1:
                leveled +=1
            if result == 2:
                errors +=1
        pending = pending - created
    print('Loops:{}-Created:{}-Leveled:{}-Errors:{}'.format(created+leveled+errors,created,leveled,errors))

def fix_document_length():
    reported = 0
    fixed = 0
    limit = Person.objects.annotate(text_len=Length('identification')).filter(text_len__lt=10).count()
    limit = random.randint(0, limit)
    #mp.Person.objects.annotate(text_len=Length('identification')).filter(text_len__gt=10).count()
    #mp.Person.objects.annotate(text_len=Length('identification')).filter(text_len__lte=9).count()
    #persons = Person.objects.all().order_by(Length('identification').asc())
    persons = Person.objects.annotate(text_len=Length('identification')).filter(text_len__lt=10)[:limit]
    print('Filtrados {}'.format(persons.count()))
    for p in persons:
        if len(p.identification) == 9:
            new_identification = create_identification()
            try:
                person_filtered = Person.objects.get(identification=new_identification)
            except:
                p.identification = new_identification
                p.save()
                fixed += 1
            print('Fixes {} Fixed {} {}%'.format(limit, fixed, fixed/limit*100))

    print('Fixes {} Fixed {}'.format(limit, fixed))

def level_persons(limit):
    leveled = 0
    persons = create_multiple_persons(10)
    for p in persons:
        try:
            person_filtered = Person.objects.get(identification=p.identification)
            person_filtered.level +=1
            if person_filtered.level > 10: person_filtered.level = 10
            person_filtered.save()
            leveled += 1
        except:
            pass

    print('Limit {} Leveled {}'.format(limit, leveled))

def daily_update():
    fix_document_length()
    ap()
    level_persons(1000)
    total_persons = Person.objects.count()
    level_0_persons = Person.objects.filter(level=0).count()
    leveled_persons = total_persons - level_0_persons
    print('Leveled {}-Level0 {}-Total {}'.format(leveled_persons, level_0_persons, total_persons))
