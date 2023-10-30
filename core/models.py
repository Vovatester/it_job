from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.db import (
    models,
)
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
)


def calculate_age(born):
    return (
        date.today().year
        - born.year
        - ((date.today().month, date.today().day) < (born.month, born.day))
    )


def min_length_validator(char_count):
    return MinLengthValidator(
        char_count,
        f'Количество символов должно быть не менее {char_count}',
    )


def password_regex_validator():
    return RegexValidator(
        regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)[A-Za-z\d\W]{8,}$',
        message='Пароль должен состоять из 8 символов, строчной и заглавной буквы, цифры и специального символа',
    )


class DateTimeMixin(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(verbose_name='Страна', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(verbose_name='Город', max_length=100)
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
        validators=[min_length_validator(8)],
    )
    password = models.CharField(
        verbose_name='Пароль', max_length=20, validators=[password_regex_validator()]
    )
    name = models.CharField(
        verbose_name='Наименование компании',
        max_length=100,
        validators=[min_length_validator(4)],
    )
    country = models.ForeignKey(
        Country, verbose_name='Страна', on_delete=models.CASCADE
    )
    town = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    foundation_date = models.DateField(verbose_name='Дата основания компании')
    site_href = models.CharField(verbose_name='Сайт', max_length=200)

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
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)

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
        validators=[min_length_validator(8)],
    )
    password = models.CharField(
        verbose_name='Пароль', max_length=20, validators=[password_regex_validator()]
    )
    name = models.CharField(
        verbose_name='Имя', max_length=100, validators=[min_length_validator(2)]
    )
    surname = models.CharField(
        verbose_name='Фамилия', max_length=100, validators=[min_length_validator(2)]
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=100,
        blank=True,
        validators=[min_length_validator(2)],
    )
    born_date = models.DateField(verbose_name='Дата рождения', default=None)
    country = models.ForeignKey(
        Country, verbose_name='Страна', on_delete=models.CASCADE
    )
    town = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    technologies = models.ManyToManyField(
        Technology, verbose_name='Технологии', through='SpecialistTechnology'
    )

    def clean(self):
        if calculate_age(born=self.born_date) < 18:
            raise ValidationError('Специалисты младше 18 лет не регистрируются')

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'
        constraints = [
            models.CheckConstraint(
                check=models.Q(born_date__lte=date.today()),
                name='born_date_constraint',
            ),
        ]

    def __str__(self):
        return self.name


class Vacancy(DateTimeMixin):
    name = models.CharField(
        verbose_name='Должность', max_length=100, validators=[min_length_validator(2)]
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Компания',
        on_delete=models.CASCADE,
    )
    town = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    salary = models.CharField(verbose_name='Зарплата', max_length=100)
    description = models.TextField(verbose_name='Описание', max_length=10000)
    published_datetime = models.DateTimeField(
        verbose_name='Дата и время публикации', blank=True, null=True, default=None
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.name


class Resume(DateTimeMixin):
    position = models.CharField(verbose_name='Должность', max_length=150)
    specialist = models.ForeignKey(
        Specialist,
        verbose_name='Специалист',
        on_delete=models.CASCADE,
    )
    salary = models.CharField(verbose_name='Зарплата', max_length=100)
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
