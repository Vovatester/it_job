import datetime
from django.db import models
from django.core.validators import MinLengthValidator


class DateTimeMixin(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(DateTimeMixin):
    login = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            MinLengthValidator(8, 'Поле "login" должно содержать минимум 8 символов')
        ],
    )
    password = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(8, 'Поле "password" должно содержать минимум 8 символов')
        ],
    )
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(4, 'Поле "name" должно содержать минимум 4 символов')
        ],
    )
    countries = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    foundation_date = models.DateField()
    site_href = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(foundation_date__lte=datetime.date.today()),
                name="foundation_date_constraint",
            ),
        ]


class Technology(DateTimeMixin):
    technology = models.CharField(max_length=100)


class Specialist(DateTimeMixin):
    login = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            MinLengthValidator(8, 'Поле "login" должно содержать минимум 8 символов')
        ],
    )
    password = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(8, 'Поле "password" должно содержать минимум 8 символов')
        ],
    )
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, 'Поле "name" должно содержать минимум 2 символа')
        ],
    )
    surname = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, 'Поле "surname" должно содержать минимум 2 символа')
        ],
    )
    patronymic = models.CharField(
        max_length=100,
        blank=True,
        validators=[
            MinLengthValidator(
                2, 'Поле "patronymic" должно содержать минимум 2 символа'
            )
        ],
    )
    born_date = models.DateField(default=None)
    technologies = models.ManyToManyField(Technology)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(born_date__lte=datetime.date.today()),
                name="born_date_constraint",
            ),
        ]


class Vacancy(DateTimeMixin):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(4, 'Поле "name" должно содержать минимум 2 символа')
        ],
    )
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    town = models.CharField(max_length=150)
    salary = models.PositiveIntegerField()
    description = models.TextField(max_length=10000)
    published_datetime = models.DateTimeField(auto_now_add=True)


class Resume(DateTimeMixin):
    position = models.CharField(max_length=150)
    specialist = models.OneToOneField(Specialist, on_delete=models.CASCADE)
    salary = models.PositiveIntegerField()
    published_datetime = models.DateTimeField(auto_now_add=True)
