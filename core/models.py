import datetime
from django.db import (
    models,
)
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
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
    country = models.CharField(verbose_name='Страна', max_length=50)
    town = models.CharField(verbose_name='Город', max_length=50)
    foundation_date = models.DateField(verbose_name='Дата основания компании')
    site_href = models.CharField(verbose_name='Сайт', max_length=200)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        constraints = [
            models.CheckConstraint(
                check=models.Q(foundation_date__lte=datetime.date.today()),
                name='foundation_date_constraint',
            ),
        ]


class Technology(DateTimeMixin):
    technology = models.CharField(verbose_name='Технологии', max_length=100)

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'


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
    technologies = models.ManyToManyField(Technology)

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'
        constraints = [
            models.CheckConstraint(
                check=models.Q(born_date__lte=datetime.date.today()),
                name='born_date_constraint',
            ),
        ]


class Vacancy(DateTimeMixin):
    name = models.CharField(
        verbose_name='Должность', max_length=100, validators=[min_length_validator(2)]
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )
    town = models.CharField(verbose_name='Город', max_length=150)
    salary = models.PositiveIntegerField(verbose_name='Зарплата')
    description = models.TextField(verbose_name='Описание', max_length=10000)
    published_datetime = models.DateTimeField(
        verbose_name='Дата и время публикации', auto_now_add=True
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Resume(DateTimeMixin):
    position = models.CharField(verbose_name='Должность', max_length=150)
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
    )
    salary = models.CharField(verbose_name='Зарплата', max_length=100)
    published_datetime = models.DateTimeField(
        verbose_name='Дата и время публикации', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
