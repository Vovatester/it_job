from datetime import date

from dateutil.relativedelta import relativedelta
from factory import LazyAttribute, Sequence, Faker, SubFactory
from factory.fuzzy import FuzzyChoice
from factory.django import DjangoModelFactory
from faker import Faker as Fk
from core.models import (
    Country,
    Town,
    Company,
    Specialist,
    Resume,
    Technology,
    Vacancy,
    SpecialistTechnology,
    RUB,
    EUR,
    USD,
)

faker = Fk('ru_RU')

technologies_names = ['Python', 'C', "C++", 'Java', 'JavaScript']


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = LazyAttribute(lambda _: faker.unique.country())


class TownFactory(DjangoModelFactory):
    class Meta:
        model = Town

    name = LazyAttribute(lambda _: faker.unique.city())
    country = SubFactory(CountryFactory)


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    login = LazyAttribute(lambda _: faker.unique.user_name())
    password = LazyAttribute(lambda _: faker.password(length=8))
    name = Faker('company')
    foundation_date = LazyAttribute(lambda _: faker.date())
    site_href = LazyAttribute(lambda _: faker.url())
    country = SubFactory(CountryFactory)
    town = SubFactory(TownFactory)


class TechnologyFactory(DjangoModelFactory):
    class Meta:
        model = Technology

    name = Sequence(lambda pk: f'technology_{pk}')


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
    country = SubFactory(CountryFactory)
    town = SubFactory(TownFactory)


class SpecialistTechnologyFactory(DjangoModelFactory):
    class Meta:
        model = SpecialistTechnology

    specialist = SubFactory(SpecialistFactory)
    technology = SubFactory(TechnologyFactory)


class VacancyFactory(DjangoModelFactory):
    class Meta:
        model = Vacancy

    name = LazyAttribute(lambda _: faker.job())
    company = SubFactory(CompanyFactory)
    town = SubFactory(TownFactory)
    salary = FuzzyChoice(
        choices=['10000', '45000', '10000-15000', '13200', '55000', '1100-1400']
    )
    salary_currency = FuzzyChoice(choices=[USD, RUB, EUR])
    description = LazyAttribute(lambda _: faker.text(max_nb_chars=300))


class ResumeFactory(DjangoModelFactory):
    class Meta:
        model = Resume

    position = LazyAttribute(lambda _: faker.job())
    salary_currency = FuzzyChoice(choices=[USD, RUB, EUR])
    salary = FuzzyChoice(
        choices=['10000', '45000', '10000-15000', '13200', '55000', '1100-1400']
    )
    description = LazyAttribute(lambda _: faker.text(max_nb_chars=300))
    specialist = SubFactory(SpecialistFactory)
