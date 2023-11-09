from datetime import date
from random import choice, randint

from dateutil.relativedelta import relativedelta
from django.core.management import BaseCommand
from faker import Faker

from core.models import (
    CURRENCY,
    Country,
    Town,
    Company,
    Specialist,
    Resume,
    Technology,
    Vacancy,
    SpecialistTechnology,
)


class Command(BaseCommand):
    technologies_name = ['Python', 'C', "C++", 'Java', 'JavaScript']
    batch_size = 500
    towns_in_every_country = 10
    companies_count = 10
    countries_count = 10
    specialists_count = 10

    help = 'Генерация тестовых записей'
    faker = Faker('ru_RU')

    def handle(self, *args, **kwargs):
        self.insert_countries()
        self.insert_cities()
        self.insert_companies()
        self.insert_specialists()
        self.insert_resumes()
        self.insert_technologies()
        self.insert_specialist_technology()
        self.insert_vacancies()

    def insert_countries(self):
        objs = (
            Country(name=self.faker.unique.country())
            for _ in range(self.countries_count)
        )
        Country.objects.bulk_create(objs=objs, batch_size=self.batch_size)

    def insert_cities(self):
        for country in Country.objects.all():
            objs = (
                Town(name=self.faker.unique.city(), country_id=country.pk)
                for _ in range(self.towns_in_every_country)
            )
            Town.objects.bulk_create(objs=objs, batch_size=self.batch_size)

    def insert_companies(self):
        towns = Town.objects.values('country_id', 'id')
        objs = (
            Company(
                login=self.faker.unique.user_name(),
                password=self.faker.password(length=8),
                name=self.faker.name(),
                foundation_date=self.faker.date(),
                site_href=self.faker.url(),
                country_id=country_id,
                town_id=choice(
                    [town['id'] for town in towns if town['country_id'] == country_id]
                ),
            )
            for country_id in range(1, self.companies_count + 1)
        )
        Company.objects.bulk_create(objs=objs, batch_size=self.batch_size)

    def insert_specialists(self):
        start_born_date = date(1970, 1, 1)
        end_born_date = date.today() - relativedelta(years=18)
        towns = Town.objects.values('id', 'country_id')
        objs = (
            Specialist(
                login=self.faker.unique.user_name(),
                password=self.faker.password(length=8),
                name=self.faker.first_name(),
                surname=self.faker.last_name(),
                patronymic=self.faker.middle_name(),
                born_date=self.faker.date_between(
                    start_date=start_born_date, end_date=end_born_date
                ),
                country_id=country_id,
                town_id=choice(
                    [town['id'] for town in towns if town['country_id'] == country_id]
                ),
            )
            for country_id in range(1, self.specialists_count + 1)
        )
        Specialist.objects.bulk_create(objs=objs, batch_size=self.batch_size)

    def insert_specialist_technology(self):
        objs = (
            SpecialistTechnology(
                specialist_id=specialist_id,
                technology_id=randint(1, len(self.technologies_name)),
            )
            for specialist_id in range(1, self.specialists_count + 1)
        )
        SpecialistTechnology.objects.bulk_create(objs=objs, batch_size=self.batch_size)

    def insert_resumes(self):
        objs = (
            Resume(
                position=self.faker.job(),
                salary_currency=choice(CURRENCY),
                salary=randint(1000, 100000),
                description=self.faker.text(max_nb_chars=1500),
                specialist_id=specialist_id,
            )
            for specialist_id in range(1, self.specialists_count + 1)
        )
        Resume.objects.bulk_create(objs=objs, batch_size=self.batch_size)

    def insert_technologies(self):
        objs = (Technology(name=technology) for technology in self.technologies_name)
        Technology.objects.bulk_create(objs=objs, batch_size=self.batch_size)

    def insert_vacancies(self):
        towns = Town.objects.values('id', 'country_id')
        objs = (
            Vacancy(
                name=self.faker.job(),
                salary_currency=choice(CURRENCY),
                salary=randint(1000, 20000),
                description=self.faker.text(max_nb_chars=1500),
                company_id=identifier,
                town_id=choice(
                    [town['id'] for town in towns if town['country_id'] == identifier]
                ),
            )
            for identifier in range(1, self.companies_count + 1)
        )
        Vacancy.objects.bulk_create(objs=objs, batch_size=self.batch_size)
