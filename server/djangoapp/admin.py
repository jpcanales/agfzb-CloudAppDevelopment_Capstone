from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
# CarModelAdmin class
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'country']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake, CarMakeAdmin)