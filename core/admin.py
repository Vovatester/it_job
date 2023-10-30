from django.contrib import admin

from .models import (
    Country,
    City,
    Company,
    Technology,
    Specialist,
    Vacancy,
    Resume,
    SpecialistTechnology,
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

    list_filter = ('name',)
    search_fields = ('name',)


class CityAdminInlines(admin.StackedInline):
    model = City
    extra = 1


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [CityAdminInlines]
    list_display = ('name',)

    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'town', 'foundation_date', 'site_href')

    list_filter = ('name', 'country', 'town')
    search_fields = ('name', 'country', 'town')


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)

    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    class SpecialistTechnologyInline(admin.StackedInline):
        model = SpecialistTechnology
        extra = 1

    inlines = (SpecialistTechnologyInline,)
    list_display = ('name', 'surname', 'patronymic', 'country', 'town')

    list_filter = ('name', 'surname', 'country', 'town')
    search_fields = ('name', 'surname', 'country', 'town')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    exclude = ('published_datetime',)
    list_display = ('name', 'company', 'town', 'salary', 'description')

    list_filter = ('name', 'company', 'town', 'salary')
    search_fields = ('name', 'company', 'town', 'salary')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    exclude = ('published_datetime',)
    list_display = ('position', 'specialist', 'salary')

    list_filter = ('position', 'specialist', 'salary')
    search_fields = ('position', 'specialist', 'salary')
