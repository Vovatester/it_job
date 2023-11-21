from datetime import date
from random import choice, randint

from dateutil.relativedelta import relativedelta
from factory import LazyAttribute, Sequence, Iterator, Faker
from factory.django import DjangoModelFactory
from django.core.management import BaseCommand
from faker import Faker as Fk

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


def salary_choice():
    salary_digit = str(randint(1000, 100000))
    salary_range = f'{salary_digit}-{int(salary_digit) + randint(1000, 30000)}'
    salary_choices = choice([salary_digit, salary_range])
    return salary_choices


faker = Fk('ru_RU')

technologies_names = ['Python', 'C', "C++", 'Java', 'JavaScript']
test_data_count = 100


class Command(BaseCommand):
    help = 'Генерация тестовых записей'

    def handle(self, *args, **kwargs):
        CountryFactory.create_batch(test_data_count)
        TownFactory.create_batch(test_data_count)
        CompanyFactory.create_batch(test_data_count)
        TechnologyFactory.create_batch(len(technologies_names))
        SpecialistFactory.create_batch(test_data_count)
        SpecialistTechnologyFactory.create_batch(test_data_count)
        VacancyFactory.create_batch(test_data_count)
        ResumeFactory.create_batch(test_data_count)


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = LazyAttribute(lambda _: faker.unique.country())


class TownFactory(DjangoModelFactory):
    class Meta:
        model = Town

    name = LazyAttribute(lambda _: faker.unique.city())
    country_id = Sequence(lambda n: test_data_count - n)


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    login = LazyAttribute(lambda _: faker.unique.user_name())
    password = LazyAttribute(lambda _: faker.password(length=8))
    name = Faker('company')
    foundation_date = LazyAttribute(lambda _: faker.date())
    site_href = LazyAttribute(lambda _: faker.url())
    country_id = Sequence(lambda n: test_data_count - n)
    town_id = Sequence(lambda n: test_data_count - n)


class TechnologyFactory(DjangoModelFactory):
    class Meta:
        model = Technology

    name = Iterator(technologies_names)


class SpecialistFactory(DjangoModelFactory):
    class Meta:
        model = Specialist

    login = LazyAttribute(lambda _: faker.unique.user_name())
    password = LazyAttribute(lambda _: faker.password(length=8))
    name = LazyAttribute(lambda _: faker.unique.first_name())
    surname = LazyAttribute(lambda _: faker.unique.last_name())
    patronymic = LazyAttribute(lambda _: faker.middle_name())
    born_date = LazyAttribute(
        lambda _: faker.date_between(
            start_date=date(1970, 1, 1),
            end_date=date.today() - relativedelta(years=18),
        )
    )
    country_id = Sequence(lambda n: test_data_count - n)
    town_id = Sequence(lambda n: test_data_count - n)


class SpecialistTechnologyFactory(DjangoModelFactory):
    class Meta:
        model = SpecialistTechnology

    specialist_id = Sequence(lambda n: test_data_count - n)
    technology_id = Sequence(lambda _: randint(1, len(technologies_names)))


class VacancyFactory(DjangoModelFactory):
    class Meta:
        model = Vacancy

    name = LazyAttribute(lambda _: faker.unique.first_name())
    salary_currency = LazyAttribute(lambda _: choice(CURRENCY)[1])
    salary = LazyAttribute(lambda _: salary_choice())
    description = LazyAttribute(lambda _: faker.text(max_nb_chars=1500))
    company_id = Sequence(lambda n: test_data_count - n)
    town_id = Sequence(lambda n: test_data_count - n)


class ResumeFactory(DjangoModelFactory):
    class Meta:
        model = Resume

    position = LazyAttribute(lambda _: faker.job())
    salary_currency = LazyAttribute(lambda _: choice(CURRENCY)[1])
    salary = LazyAttribute(lambda _: salary_choice())
    description = LazyAttribute(lambda _: faker.text(max_nb_chars=1500))
    specialist_id = Sequence(lambda n: test_data_count - n)
