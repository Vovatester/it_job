from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    MaxLengthValidator,
)

RUB = 'RUB'
USD = 'USD'
EUR = 'EUR'
CURRENCY = [(RUB, 'RUB'), (USD, 'USD'), (EUR, 'EUR')]

password_regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)[A-Za-z\d\W]{8,}$'

min_age = 18


def min_born_date_validator(born_date: date) -> date | ValidationError:
    today = date.today()
    age_18 = today - relativedelta(years=min_age)
    if born_date > age_18:
        raise ValidationError('Возраст специалиста не может быть меньше 18 лет')
    return born_date


class DateTimeMixin(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(
        verbose_name='Страна',
        unique=True,
        max_length=50,
        validators=[MaxLengthValidator(50)],
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(
        verbose_name='Город',
        max_length=100,
        validators=[MaxLengthValidator(100)],
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        unique_together = ('name', 'country')

    def __str__(self):
        return self.name


class Company(DateTimeMixin):
    login = models.CharField(
        verbose_name='Логин',
        max_length=30,
        unique=True,
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(30),
        ],
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=20,
        validators=[RegexValidator(regex=password_regex), MaxLengthValidator(20)],
    )
    name = models.CharField(
        verbose_name='Наименование компании',
        max_length=100,
        validators=[MinLengthValidator(4), MaxLengthValidator(100)],
    )
    country = models.ForeignKey(
        Country, verbose_name='Страна', on_delete=models.CASCADE
    )
    town = models.ForeignKey(Town, verbose_name='Город', on_delete=models.CASCADE)
    foundation_date = models.DateField(verbose_name='Дата основания компании')
    site_href = models.URLField(
        verbose_name='Сайт',
        max_length=200,
        validators=[MaxLengthValidator(200)],
    )

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        constraints = [
            models.CheckConstraint(
                check=models.Q(foundation_date__lte=date.today()),
                name='foundation_date_constraint',
            ),
        ]

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        unique=True,
        validators=[MaxLengthValidator(100)],
    )

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'

    def __str__(self):
        return self.name


class Specialist(DateTimeMixin):
    login = models.CharField(
        verbose_name='Логин',
        max_length=30,
        unique=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(30)],
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=20,
        validators=[RegexValidator(regex=password_regex), MaxLengthValidator(20)],
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=100,
        blank=True,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
    )
    born_date = models.DateField(
        verbose_name='Дата рождения', default=None, validators=[min_born_date_validator]
    )
    country = models.ForeignKey(
        Country, verbose_name='Страна', on_delete=models.CASCADE
    )
    town = models.ForeignKey(Town, verbose_name='Город', on_delete=models.CASCADE)
    technologies = models.ManyToManyField(
        Technology, verbose_name='Технологии', through='SpecialistTechnology'
    )

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    born_date__lte=date.today() - relativedelta(years=min_age),
                ),
                name='born_date_constraint',
            ),
        ]

    def __str__(self):
        return self.name


class Vacancy(DateTimeMixin):
    name = models.CharField(
        verbose_name='Должность',
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Компания',
        on_delete=models.CASCADE,
    )
    town = models.ForeignKey(Town, verbose_name='Город', on_delete=models.CASCADE)
    salary = models.CharField(
        verbose_name='Зарплата',
        max_length=100,
        validators=[MaxLengthValidator(100)],
    )
    salary_currency = models.CharField(
        verbose_name='Валюта',
        choices=CURRENCY,
        default=RUB,
        max_length=3,
        validators=[MaxLengthValidator(3)],
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=10000,
        validators=[MaxLengthValidator(10000)],
    )
    published_datetime = models.DateTimeField(
        verbose_name='Дата и время публикации', blank=True, null=True, default=None
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.name


class Resume(DateTimeMixin):
    position = models.CharField(
        verbose_name='Должность',
        max_length=150,
        validators=[MaxLengthValidator(150)],
    )
    specialist = models.ForeignKey(
        Specialist,
        verbose_name='Специалист',
        on_delete=models.CASCADE,
    )
    salary = models.CharField(
        verbose_name='Зарплата',
        max_length=100,
        validators=[MaxLengthValidator(100)],
    )
    salary_currency = models.CharField(
        verbose_name='Валюта',
        choices=CURRENCY,
        default=RUB,
        max_length=3,
        validators=[MaxLengthValidator(3)],
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=10000,
        validators=[MaxLengthValidator(10000)],
    )
    published_datetime = models.DateTimeField(
        verbose_name='Дата и время публикации',
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    def __str__(self):
        return self.position


class SpecialistTechnology(models.Model):
    specialist = models.ForeignKey(
        Specialist, verbose_name='Специалист', on_delete=models.CASCADE
    )
    technology = models.ForeignKey(
        Technology, verbose_name='Технология', on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('specialist', 'technology')
        verbose_name = 'Технология специалиста'
        verbose_name_plural = 'Технологии специалиста'


class Token(models.Model):
    specialist = models.ForeignKey(
        Specialist, verbose_name='Cпециалист', on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company, verbose_name='Компания', on_delete=models.CASCADE
    )
    token = models.CharField(
        verbose_name='token', max_length=200, validators=[MaxLengthValidator(200)]
    )
