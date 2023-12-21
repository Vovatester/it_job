from random import choice

from django.core.management import BaseCommand

from core.models import (
    Country,
    Town,
    Company,
    Specialist,
    Resume,
    Technology,
    Vacancy,
)
from core.tests.factories import (
    CountryFactory,
    TownFactory,
    CompanyFactory,
    TechnologyFactory,
    SpecialistFactory,
    SpecialistTechnologyFactory,
    VacancyFactory,
    ResumeFactory,
)
from core.data import TECHNOLOGIES

countries_count = 15
towns_count_in_every_country = 10
companies_count = 200
specialists_count = 20
specialist_technologies_count = 3
company_vacancies_count = 2
specialists_resumes_count = 2


class Command(BaseCommand):
    def handle(self, *args, **options):
        countries = self.insert_countries()
        towns = self.insert_towns(countries=countries)
        companies = self.insert_companies(towns=towns)
        technologies = self.insert_technologies()
        specialists = self.insert_specialists(towns=towns, technologies=technologies)
        self.insert_vacancies(companies=companies)
        self.insert_resumes(specialists=specialists)

    @staticmethod
    def insert_countries() -> list[Country]:
        return CountryFactory.create_batch(size=countries_count)

    @staticmethod
    def insert_towns(countries: list[Country]) -> list[Town]:
        towns = []
        for country in countries:
            for _ in range(towns_count_in_every_country):
                towns.append(TownFactory(country=country))

        return towns

    @staticmethod
    def insert_companies(towns: list[Town]) -> list[Company]:
        companies = []
        for _ in range(companies_count):
            town = choice(towns)
            companies.append(CompanyFactory(town=town, country=town.country))

        return companies

    @staticmethod
    def insert_technologies() -> list[Technology]:
        technologies = []
        for technology in TECHNOLOGIES:
            technologies.append(TechnologyFactory(name=technology))

        return technologies

    @staticmethod
    def insert_specialists(
        towns: list[Town], technologies: list[Technology]
    ) -> list[Specialist]:
        specialists = []
        specialist_technology = []
        specialist_tech = []
        for _ in range(specialists_count):
            town = choice(towns)
            specialists.append(SpecialistFactory(town=town, country=town.country))

            for _ in range(specialist_technologies_count):
                technology = choice(technologies)
                while technology in specialist_tech:
                    technology = choice(technologies)
                specialist_tech.append(technology)
                specialist_technology.append(
                    SpecialistTechnologyFactory(
                        specialist=specialists[-1], technology=technology
                    )
                )
            specialist_tech = []
        return specialists

    @staticmethod
    def insert_vacancies(companies: list[Company]) -> list[Vacancy]:
        vacancies = []
        for company in companies:
            for _ in range(company_vacancies_count):
                vacancies.append(VacancyFactory(company=company, town=company.town))

        return vacancies

    @staticmethod
    def insert_resumes(specialists: list[Specialist]) -> list[Resume]:
        resumes = []
        for specialist in specialists:
            for _ in range(specialists_resumes_count):
                resumes.append(ResumeFactory(specialist=specialist))

        return resumes
